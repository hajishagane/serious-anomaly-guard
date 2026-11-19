import os
import joblib
import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import OperationalError
import pandas as pd

from database import init_db, SessionLocal, Transaction
from features import compute_velocity_features, FEATURE_NAMES
from dashboard import DASHBOARD_HTML

app = FastAPI(title="Anomaly Guard", version="1.1.0")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app.router.lifespan_context = lifespan

MODEL_PATH = Path(os.getenv("MODEL_PATH", "model.joblib"))
MODEL = None
THRESHOLD = 0.50

try:
    if MODEL_PATH.exists():
        bundle = joblib.load(MODEL_PATH)
        MODEL = bundle["model"]
        THRESHOLD = float(bundle.get("threshold", 0.50))
        print(f"Model successfully loaded from {MODEL_PATH} (threshold={THRESHOLD})")
    else:
        print(f"WARNING: Model artifact not found at {MODEL_PATH}. Using fallback.")
except Exception as e:
    print(f"WARNING: Failed to load model from {MODEL_PATH}: {e}. Using fallback.")


class TransactionInput(BaseModel):
    tx_id: str
    origin_account_id: str
    vendor_hash: str
    amount_kes: float
    timestamp: datetime
    oldbalance_org: float = 0.0
    newbalance_orig: float = 0.0
    newbalance_dest: float = 0.0
    oldbalance_dest: Optional[float] = None
    tx_type: Optional[str] = "PAYMENT"


class ThresholdInput(BaseModel):
    threshold: float = Field(..., ge=0.05, le=0.95)


def recommend_action(score: float, verdict: int, threshold: float) -> str:
    if verdict == 1:
        if score >= max(0.85, threshold + 0.08):
            return "HOLD_AND_ESCALATE_SOC"
        return "FLAG_FOR_MANUAL_REVIEW"
    if score >= max(0.30, threshold - 0.20):
        return "ALLOW_WITH_MONITORING"
    return "ALLOW"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": MODEL is not None,
        "database": "connected",
        "threshold": THRESHOLD,
    }


@app.get("/settings")
def get_settings():
    return {"threshold": THRESHOLD}


@app.post("/settings/threshold")
def update_threshold(payload: ThresholdInput):
    global THRESHOLD
    THRESHOLD = round(float(payload.threshold), 2)
    return {"status": "updated", "threshold": THRESHOLD}


@app.post("/score")
def score_transaction(payload: TransactionInput):
    session = SessionLocal()
    try:
        # Normalize to offset-naive datetime for safe SQLite arithmetic
        ts = payload.timestamp.replace(tzinfo=None)

        # 1. Compute velocity features from SQLite 24-hour history
        tsl, c15, c24 = compute_velocity_features(
            session, payload.origin_account_id, ts, Transaction
        )

        # 2. Build 10-feature model vector
        orig_balance_zeroed = int(payload.oldbalance_org == 0)
        amount_over_orig_balance = float(payload.amount_kes > payload.oldbalance_org)
        balance_change_orig = payload.oldbalance_org - payload.newbalance_orig
        dest_balance_after = payload.newbalance_dest

        features = [
            payload.amount_kes,
            tsl,
            c15,
            c24,
            ts.hour,
            int(ts.weekday() >= 5),
            orig_balance_zeroed,
            amount_over_orig_balance,
            balance_change_orig,
            dest_balance_after,
        ]

        # 3. ML inference + verifiable behavioral & ledger-integrity checks
        if MODEL is not None:
            X_input = pd.DataFrame([features], columns=FEATURE_NAMES)
            ml_prob = float(MODEL.predict_proba(X_input.values)[0][1])
        else:
            ml_prob = 0.05

        behavioral_risk = 0.0
        signals = []

        if ml_prob >= 0.30:
            signals.append(
                f"ML model detected anomalous feature pattern (raw model score: {ml_prob:.2f})."
            )

        # Rapid structuring / smurfing burst (3+ prior tx in 15 min)
        if c15 >= 3:
            behavioral_risk = max(behavioral_risk, min(0.97, 0.84 + 0.04 * (c15 - 3)))
            signals.append(
                f"High short-window velocity: {c15} prior transactions by this account in the last 15 minutes (structuring / smurfing pattern)."
            )

        # High-value full account drain (SIM-swap / mule sweep)
        if (
            payload.oldbalance_org >= 50000
            and payload.newbalance_orig == 0
            and payload.amount_kes >= 50000
        ):
            is_ghost_hour = ts.hour <= 4
            behavioral_risk = max(
                behavioral_risk, 0.92 if (is_ghost_hour or payload.amount_kes >= 200000) else 0.85
            )
            signals.append(
                f"Origin account drained to KES 0.00 on a high-value movement (KES {payload.amount_kes:,.2f})."
            )

        # Overdraft vs. sender ledger reconciliation mismatch
        if payload.oldbalance_org > 0 and payload.amount_kes > payload.oldbalance_org:
            behavioral_risk = max(behavioral_risk, 0.88)
            signals.append(
                f"Transfer amount (KES {payload.amount_kes:,.2f}) exceeds recorded sender pre-transaction balance (KES {payload.oldbalance_org:,.2f})."
            )
        elif (
            payload.oldbalance_org > 0
            and abs((payload.oldbalance_org - payload.amount_kes) - payload.newbalance_orig) > 1.0
        ):
            expected_orig = payload.oldbalance_org - payload.amount_kes
            behavioral_risk = max(behavioral_risk, 0.85)
            signals.append(
                f"Sender balance reconciliation mismatch: KES {payload.oldbalance_org:,.2f} minus KES {payload.amount_kes:,.2f} should leave KES {expected_orig:,.2f}, but new balance is KES {payload.newbalance_orig:,.2f}."
            )

        # Optional receiver balance reconciliation check
        if (
            payload.oldbalance_dest is not None
            and payload.oldbalance_dest > 0
            and abs((payload.oldbalance_dest + payload.amount_kes) - payload.newbalance_dest) > 1.0
        ):
            expected_dest = payload.oldbalance_dest + payload.amount_kes
            behavioral_risk = max(behavioral_risk, 0.83)
            signals.append(
                f"Receiver balance reconciliation mismatch: expected KES {expected_dest:,.2f}, recorded KES {payload.newbalance_dest:,.2f}."
            )

        # Ghost-hour context signal
        if ts.hour <= 4 and payload.amount_kes >= 20000:
            signals.append(
                f"Off-hours / ghost-hour activity recorded at {ts.strftime('%H:%M')} local time."
            )

        if not signals:
            signals.append(
                "Transaction amount, ledger balance reconciliation, and account velocity fall within normal behavioral bounds."
            )

        score = round(min(0.999, max(ml_prob, behavioral_risk)), 4)
        verdict = int(score >= THRESHOLD)
        action = recommend_action(score, verdict, THRESHOLD)

        # 4. Persist to SQLite audit log
        db_tx = Transaction(
            tx_id=payload.tx_id,
            origin_account_id=payload.origin_account_id,
            vendor_hash=payload.vendor_hash,
            amount_kes=payload.amount_kes,
            timestamp=ts,
            tx_count_15min=c15,
            tx_count_24h=c24,
            time_since_last_tx=tsl,
            verdict=verdict,
            score=score,
        )
        session.add(db_tx)
        try:
            session.commit()
        except (sqlite3.IntegrityError, Exception) as e:
            session.rollback()
            existing = session.query(Transaction).filter_by(tx_id=payload.tx_id).first()
            if existing:
                return {
                    "tx_id": existing.tx_id,
                    "verdict": existing.verdict,
                    "score": existing.score,
                    "threshold": THRESHOLD,
                    "recommended_action": recommend_action(existing.score, existing.verdict, THRESHOLD),
                    "signals": signals,
                    "features": {
                        "time_since_last_tx": existing.time_since_last_tx,
                        "tx_count_15min": existing.tx_count_15min,
                        "tx_count_24h": existing.tx_count_24h,
                    },
                }
            raise e

        return {
            "tx_id": payload.tx_id,
            "verdict": verdict,
            "score": score,
            "threshold": THRESHOLD,
            "recommended_action": action,
            "signals": signals,
            "features": {
                "time_since_last_tx": tsl,
                "tx_count_15min": c15,
                "tx_count_24h": c24,
            },
        }
    except OperationalError as oe:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Database operational error: {oe}")
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal scoring error: {e}")
    finally:
        session.close()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    """Serve the fraud monitoring console UI."""
    return HTMLResponse(content=DASHBOARD_HTML)


@app.get("/stats")
def stats():
    session = SessionLocal()
    try:
        total = session.query(Transaction).count()
        flagged = session.query(Transaction).filter(Transaction.verdict == 1).count()
        return {
            "total_scored": total,
            "flagged_fraud": flagged,
            "flag_rate": (flagged / total) if total else 0.0,
            "model_loaded": MODEL is not None,
            "threshold": THRESHOLD,
        }
    finally:
        session.close()


@app.get("/transactions")
def list_transactions(limit: int = 50):
    session = SessionLocal()
    try:
        rows = (
            session.query(Transaction)
            .order_by(Transaction.timestamp.desc())
            .limit(min(limit, 200))
            .all()
        )
        return {
            "transactions": [
                {
                    "tx_id": r.tx_id,
                    "origin_account_id": r.origin_account_id,
                    "vendor_hash": r.vendor_hash,
                    "amount_kes": r.amount_kes,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                    "verdict": r.verdict,
                    "score": r.score,
                }
                for r in rows
            ]
        }
    finally:
        session.close()
