import os
import joblib
import sqlite3
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from sqlalchemy.exc import OperationalError
import pandas as pd

from database import init_db, SessionLocal, Transaction
from features import compute_velocity_features, FEATURE_NAMES
from dashboard import DASHBOARD_HTML

app = FastAPI(title="Anomaly Guard", version="1.0.0")


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
        print(f"Model successfully loaded from {MODEL_PATH}")
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


class ThresholdInput(BaseModel):
    threshold: float = Field(..., ge=0.05, le=0.95)


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
        # Normalize to offset-naive datetime so SQLite comparisons never raise TypeError
        ts = payload.timestamp.replace(tzinfo=None)

        # 1. Compute velocity features from SQLite history
        tsl, c15, c24 = compute_velocity_features(
            session, payload.origin_account_id, ts, Transaction
        )

        # 2. Build feature vector (10 features)
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

        # 3. ML model inference + behavioral velocity/drain calibration
        if MODEL is not None:
            X_input = pd.DataFrame([features], columns=FEATURE_NAMES)
            prob = float(MODEL.predict_proba(X_input.values)[0][1])
        else:
            prob = 0.05

        behavioral_risk = 0.0
        # Rapid structuring / smurfing burst (e.g. >= 3 tx in 15 min)
        if c15 >= 3:
            behavioral_risk = max(behavioral_risk, min(0.96, 0.58 + 0.11 * (c15 - 2)))
        # Full account drain on significant value (especially ghost hours 00:00-04:59)
        if payload.oldbalance_org >= 50000 and payload.newbalance_orig == 0 and payload.amount_kes >= 50000:
            is_ghost_hour = ts.hour <= 4
            behavioral_risk = max(behavioral_risk, 0.86 if (is_ghost_hour or payload.amount_kes >= 200000) else 0.71)
        # Amount exceeds recorded pre-transaction balance
        if payload.oldbalance_org > 0 and payload.amount_kes > payload.oldbalance_org:
            behavioral_risk = max(behavioral_risk, 0.80)

        score = round(min(0.999, max(prob, behavioral_risk)), 4)
        verdict = int(score >= THRESHOLD)

        # 4. Log transaction
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
