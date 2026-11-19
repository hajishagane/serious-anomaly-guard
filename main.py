import csv
import io
import json
import os
import sqlite3
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError, OperationalError

from dashboard import DASHBOARD_HTML
from database import InferenceLog, SessionLocal, SystemSetting, Transaction, init_db, reset_db
from features import FEATURE_NAMES, compute_syndicate_fan_in, compute_velocity_features

app = FastAPI(
    title="Anomaly Guard API",
    description="B2B Real-Time Mobile Money Fraud Detection Prototype (PaySim-KES)",
    version="2.0.0",
)

MODEL_PATH = Path(os.getenv("MODEL_PATH", "model.joblib"))
METRICS_PATH = Path(os.getenv("METRICS_PATH", "model_metrics.json"))
SOC_ADMIN_PIN = os.getenv("SOC_ADMIN_PIN", "2026")
B2B_API_KEY = os.getenv("API_KEY", "").strip()
ENFORCE_API_KEY = os.getenv("ENFORCE_API_KEY", "false").lower() == "true"
STATIC_RULE_LIMIT_KES = 50000.0

MODEL = None
DEFAULT_THRESHOLD = 0.80
THRESHOLD = DEFAULT_THRESHOLD

try:
    if MODEL_PATH.exists():
        bundle = joblib.load(MODEL_PATH)
        MODEL = bundle["model"]
        DEFAULT_THRESHOLD = round(float(bundle.get("threshold", 0.80)), 2)
        THRESHOLD = DEFAULT_THRESHOLD
        print(f"Model successfully loaded from {MODEL_PATH} (default_threshold={DEFAULT_THRESHOLD})")
    else:
        print(f"WARNING: Model artifact not found at {MODEL_PATH}. Using fallback.")
except Exception as e:
    print(f"WARNING: Failed to load model from {MODEL_PATH}: {e}. Using fallback.")


def load_persisted_threshold() -> float:
    global THRESHOLD
    session = SessionLocal()
    try:
        setting = session.query(SystemSetting).filter_by(key="threshold").first()
        if setting:
            THRESHOLD = round(float(setting.value), 2)
        else:
            THRESHOLD = DEFAULT_THRESHOLD
            session.add(SystemSetting(key="threshold", value=str(THRESHOLD)))
            session.commit()
    except Exception:
        THRESHOLD = DEFAULT_THRESHOLD
    finally:
        session.close()
    return THRESHOLD


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    load_persisted_threshold()
    yield


app.router.lifespan_context = lifespan


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
    admin_pin: Optional[str] = None


class DispositionInput(BaseModel):
    review_status: str = Field(..., pattern="^(PENDING|CONFIRMED_FRAUD|FALSE_POSITIVE)$")


def verify_admin_pin(x_admin_token: Optional[str], body_pin: Optional[str] = None):
    supplied = (x_admin_token or body_pin or "").strip()
    if supplied != SOC_ADMIN_PIN:
        raise HTTPException(
            status_code=401,
            detail="SOC Administrator authentication required (invalid X-Admin-Token / PIN).",
        )


def verify_b2b_api_key(x_api_key: Optional[str]):
    if ENFORCE_API_KEY and B2B_API_KEY and (x_api_key or "").strip() != B2B_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header.")


def recommend_action(score: float, verdict: int, threshold: float) -> str:
    if verdict == 1:
        if score >= max(0.86, threshold + 0.06):
            return "HOLD_AND_ESCALATE_SOC"
        return "FLAG_FOR_MANUAL_REVIEW"
    if score >= max(0.30, threshold - 0.20):
        return "ALLOW_WITH_MONITORING"
    return "ALLOW"


def determine_scoring_source(ml_score: float, policy_score: float, threshold: float) -> str:
    ml_hit = ml_score >= threshold
    pol_hit = policy_score >= threshold
    if ml_hit and pol_hit:
        return "HYBRID_ML_AND_POLICY"
    if ml_hit:
        return "ML_MODEL"
    if pol_hit:
        return "POLICY_GUARDRAIL"
    return "BASELINE_CLEAR"


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_loaded": MODEL is not None,
        "database": "connected",
        "threshold": THRESHOLD,
        "static_rule_limit_kes": STATIC_RULE_LIMIT_KES,
        "b2b_api_key_enforced": bool(ENFORCE_API_KEY and B2B_API_KEY),
    }


@app.get("/settings")
def get_settings():
    return {
        "threshold": THRESHOLD,
        "default_threshold": DEFAULT_THRESHOLD,
        "static_rule_limit_kes": STATIC_RULE_LIMIT_KES,
        "admin_auth_required": True,
    }


@app.post("/settings/threshold")
def update_threshold(
    payload: ThresholdInput,
    x_admin_token: Optional[str] = Header(default=None),
):
    verify_admin_pin(x_admin_token, payload.admin_pin)
    global THRESHOLD
    THRESHOLD = round(float(payload.threshold), 2)
    session = SessionLocal()
    try:
        setting = session.query(SystemSetting).filter_by(key="threshold").first()
        if setting:
            setting.value = str(THRESHOLD)
            setting.updated_at = datetime.utcnow()
        else:
            session.add(SystemSetting(key="threshold", value=str(THRESHOLD)))
        session.commit()
    finally:
        session.close()
    return {"status": "updated", "threshold": THRESHOLD}


@app.post("/score")
def score_transaction(
    payload: TransactionInput,
    x_api_key: Optional[str] = Header(default=None),
):
    verify_b2b_api_key(x_api_key)
    t_start = time.perf_counter()
    session = SessionLocal()
    try:
        ts = payload.timestamp.replace(tzinfo=None)
        tx_type = (payload.tx_type or "PAYMENT").upper()

        # Idempotency check BEFORE velocity calculation so retries return identical payloads
        existing_tx = session.query(Transaction).filter_by(tx_id=payload.tx_id).first()
        if existing_tx:
            existing_log = session.query(InferenceLog).filter_by(tx_id=payload.tx_id).first()
            if existing_log:
                return {
                    "tx_id": existing_tx.tx_id,
                    "verdict": existing_log.binary_verdict,
                    "score": existing_log.anomaly_score,
                    "ml_score": existing_log.ml_score,
                    "policy_score": existing_log.policy_score,
                    "scoring_source": existing_log.scoring_source,
                    "static_rule_verdict": existing_log.static_rule_verdict,
                    "threshold": existing_log.threshold_used,
                    "recommended_action": existing_log.action_taken,
                    "latency_ms": existing_log.latency_ms,
                    "signals": json.loads(existing_log.triggering_features or "[]"),
                    "features": {
                        "time_since_last_tx": existing_tx.time_since_last_tx,
                        "tx_count_15min": existing_tx.tx_count_15min,
                        "tx_count_24h": existing_tx.tx_count_24h,
                        "vendor_unique_senders_15min": existing_log.vendor_unique_senders_15min,
                        "vendor_inflow_15min": existing_log.vendor_inflow_15min,
                    },
                }

        # 1. Compute sender velocity & recipient fan-in syndicate signals from SQLite
        tsl, c15, c24 = compute_velocity_features(
            session, payload.origin_account_id, ts, Transaction
        )
        vendor_other_senders, vendor_inflow_15m = compute_syndicate_fan_in(
            session, payload.vendor_hash, payload.origin_account_id, ts, Transaction
        )

        # 2. Build canonical 10-feature ML vector
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

        # 3A. ML model inference
        if MODEL is not None:
            X_input = pd.DataFrame([features], columns=FEATURE_NAMES)
            ml_score = round(float(MODEL.predict_proba(X_input.values)[0][1]), 4)
        else:
            ml_score = 0.05

        # 3B. Transparent deterministic policy & ledger-integrity guardrails
        policy_score = 0.0
        signals = []

        if ml_score >= 0.30:
            signals.append(
                f"ML classifier scored elevated transaction anomaly probability ({ml_score:.2f})."
            )

        # Smurfing / structuring burst (3+ prior tx by same sender within 15 min)
        if c15 >= 3:
            policy_score = max(policy_score, min(0.98, 0.92 + 0.02 * (c15 - 3)))
            signals.append(
                f"Velocity structuring (smurfing): {c15} prior transactions from {payload.origin_account_id} in the last 15 minutes."
            )

        # Coordinated money-mule fan-in syndicate (3+ distinct senders hitting same destination in 15 min)
        if vendor_other_senders >= 2 and tx_type in ("TRANSFER", "CASH_OUT"):
            total_cluster = vendor_inflow_15m + payload.amount_kes
            policy_score = max(policy_score, min(0.98, 0.93 + 0.02 * (vendor_other_senders - 2)))
            signals.append(
                f"Mule-ring fan-in detected: {vendor_other_senders + 1} distinct accounts routed KES {total_cluster:,.2f} into {payload.vendor_hash} within 15 minutes."
            )

        # High-value account sweep / SIM-swap drain
        if (
            payload.oldbalance_org >= 50000
            and payload.newbalance_orig == 0
            and payload.amount_kes >= 50000
        ):
            is_ghost_hour = ts.hour <= 4
            policy_score = max(
                policy_score, 0.96 if (is_ghost_hour or payload.amount_kes >= 200000) else 0.92
            )
            signals.append(
                f"Full account drain to KES 0.00 on high-value movement (KES {payload.amount_kes:,.2f})."
            )

        # Sender overdraft or ledger reconciliation mismatch
        if payload.oldbalance_org > 0 and payload.amount_kes > payload.oldbalance_org:
            policy_score = max(policy_score, 0.95)
            signals.append(
                f"Overdraft anomaly: transfer amount (KES {payload.amount_kes:,.2f}) exceeds pre-transaction balance (KES {payload.oldbalance_org:,.2f})."
            )
        elif (
            payload.oldbalance_org > 0
            and abs((payload.oldbalance_org - payload.amount_kes) - payload.newbalance_orig) > 1.0
        ):
            expected_orig = payload.oldbalance_org - payload.amount_kes
            policy_score = max(policy_score, 0.93)
            signals.append(
                f"Sender ledger mismatch: KES {payload.oldbalance_org:,.2f} - KES {payload.amount_kes:,.2f} should leave KES {expected_orig:,.2f}, recorded KES {payload.newbalance_orig:,.2f}."
            )

        # Optional receiver balance reconciliation mismatch
        if (
            payload.oldbalance_dest is not None
            and payload.oldbalance_dest > 0
            and abs((payload.oldbalance_dest + payload.amount_kes) - payload.newbalance_dest) > 1.0
        ):
            expected_dest = payload.oldbalance_dest + payload.amount_kes
            policy_score = max(policy_score, 0.92)
            signals.append(
                f"Receiver ledger mismatch: expected KES {expected_dest:,.2f}, recorded KES {payload.newbalance_dest:,.2f}."
            )

        # Ghost-hour context
        if ts.hour <= 4 and payload.amount_kes >= 20000:
            signals.append(
                f"Ghost-hour activity window ({ts.strftime('%H:%M')} local time)."
            )

        if not signals:
            signals.append(
                "Amount, ledger balance reconciliation, sender velocity, and recipient fan-in are within normal baseline."
            )

        policy_score = round(policy_score, 4)
        score = round(min(0.999, max(ml_score, policy_score)), 4)
        verdict = int(score >= THRESHOLD)
        static_rule_verdict = int(payload.amount_kes > STATIC_RULE_LIMIT_KES)
        action = recommend_action(score, verdict, THRESHOLD)
        scoring_source = determine_scoring_source(ml_score, policy_score, THRESHOLD)
        latency_ms = round((time.perf_counter() - t_start) * 1000.0, 2)

        # 4. Persist to Parsed_Transactions + ML_Inference_Log (1:1 audit link)
        db_tx = Transaction(
            tx_id=payload.tx_id,
            origin_account_id=payload.origin_account_id,
            vendor_hash=payload.vendor_hash,
            tx_type=tx_type,
            amount_kes=payload.amount_kes,
            oldbalance_org=payload.oldbalance_org,
            newbalance_orig=payload.newbalance_orig,
            oldbalance_dest=payload.oldbalance_dest,
            newbalance_dest=payload.newbalance_dest,
            timestamp=ts,
            tx_count_15min=c15,
            tx_count_24h=c24,
            time_since_last_tx=tsl,
            verdict=verdict,
            score=score,
        )
        db_log = InferenceLog(
            tx_id=payload.tx_id,
            anomaly_score=score,
            ml_score=ml_score,
            policy_score=policy_score,
            scoring_source=scoring_source,
            binary_verdict=verdict,
            static_rule_verdict=static_rule_verdict,
            threshold_used=THRESHOLD,
            action_taken=action,
            latency_ms=latency_ms,
            vendor_unique_senders_15min=vendor_other_senders,
            vendor_inflow_15min=vendor_inflow_15m,
            triggering_features=json.dumps(signals),
            review_status="PENDING",
        )
        try:
            session.add(db_tx)
            session.flush()
            session.add(db_log)
            session.commit()
        except (IntegrityError, sqlite3.IntegrityError):
            session.rollback()
            raise HTTPException(status_code=409, detail="Concurrent duplicate transaction ID.")

        return {
            "tx_id": payload.tx_id,
            "verdict": verdict,
            "score": score,
            "ml_score": ml_score,
            "policy_score": policy_score,
            "scoring_source": scoring_source,
            "static_rule_verdict": static_rule_verdict,
            "threshold": THRESHOLD,
            "recommended_action": action,
            "latency_ms": latency_ms,
            "signals": signals,
            "features": {
                "time_since_last_tx": tsl,
                "tx_count_15min": c15,
                "tx_count_24h": c24,
                "vendor_unique_senders_15min": vendor_other_senders,
                "vendor_inflow_15min": vendor_inflow_15m,
            },
        }
    except HTTPException:
        session.rollback()
        raise
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
        logs = session.query(InferenceLog).all()
        latencies = [float(l.latency_ms) for l in logs if l.latency_ms is not None]
        static_flagged = sum(1 for l in logs if l.static_rule_verdict == 1)
        caught_missed_by_static = sum(
            1 for l in logs if l.binary_verdict == 1 and l.static_rule_verdict == 0
        )
        confirmed = sum(1 for l in logs if l.review_status == "CONFIRMED_FRAUD")
        false_pos = sum(1 for l in logs if l.review_status == "FALSE_POSITIVE")
        pending = sum(1 for l in logs if l.binary_verdict == 1 and l.review_status == "PENDING")

        avg_lat = round(float(np.mean(latencies)), 2) if latencies else 0.0
        p95_lat = round(float(np.percentile(latencies, 95)), 2) if latencies else 0.0
        max_lat = round(float(np.max(latencies)), 2) if latencies else 0.0
        sla_pct = (
            round(100.0 * sum(1 for x in latencies if x <= 1500.0) / len(latencies), 1)
            if latencies
            else 100.0
        )

        return {
            "total_scored": total,
            "flagged_fraud": flagged,
            "flag_rate": (flagged / total) if total else 0.0,
            "static_rule_flagged": static_flagged,
            "caught_missed_by_static": caught_missed_by_static,
            "avg_latency_ms": avg_lat,
            "p95_latency_ms": p95_lat,
            "max_latency_ms": max_lat,
            "sla_compliance_pct": sla_pct,
            "confirmed_fraud": confirmed,
            "false_positives": false_pos,
            "pending_review": pending,
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
            session.query(Transaction, InferenceLog)
            .outerjoin(InferenceLog, Transaction.tx_id == InferenceLog.tx_id)
            .order_by(Transaction.timestamp.desc())
            .limit(min(limit, 200))
            .all()
        )
        items = []
        for tx, log in rows:
            items.append(
                {
                    "tx_id": tx.tx_id,
                    "tx_type": tx.tx_type or "PAYMENT",
                    "origin_account_id": tx.origin_account_id,
                    "vendor_hash": tx.vendor_hash,
                    "amount_kes": tx.amount_kes,
                    "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
                    "verdict": tx.verdict,
                    "score": tx.score,
                    "ml_score": log.ml_score if log else tx.score,
                    "policy_score": log.policy_score if log else 0.0,
                    "scoring_source": log.scoring_source if log else "ML_MODEL",
                    "static_rule_verdict": log.static_rule_verdict if log else int(tx.amount_kes > STATIC_RULE_LIMIT_KES),
                    "action_taken": log.action_taken if log else ("FLAG_FOR_MANUAL_REVIEW" if tx.verdict else "ALLOW"),
                    "latency_ms": log.latency_ms if log else 0.0,
                    "review_status": log.review_status if log else "PENDING",
                    "signals": json.loads(log.triggering_features) if (log and log.triggering_features) else [],
                }
            )
        return {"transactions": items}
    finally:
        session.close()


@app.patch("/logs/{tx_id}/disposition")
def update_disposition(tx_id: str, payload: DispositionInput):
    session = SessionLocal()
    try:
        log = session.query(InferenceLog).filter_by(tx_id=tx_id).first()
        if not log:
            raise HTTPException(status_code=404, detail=f"Inference log not found for {tx_id}")
        log.review_status = payload.review_status
        log.reviewed_at = datetime.utcnow()
        session.commit()
        return {
            "tx_id": tx_id,
            "review_status": log.review_status,
            "reviewed_at": log.reviewed_at.isoformat(),
        }
    finally:
        session.close()


@app.get("/accounts/{account_id}")
def account_timeline(account_id: str):
    session = SessionLocal()
    try:
        rows = (
            session.query(Transaction, InferenceLog)
            .outerjoin(InferenceLog, Transaction.tx_id == InferenceLog.tx_id)
            .filter(
                or_(
                    Transaction.origin_account_id == account_id,
                    Transaction.vendor_hash == account_id,
                )
            )
            .order_by(Transaction.timestamp.desc())
            .limit(100)
            .all()
        )
        total_out = sum(tx.amount_kes for tx, _ in rows if tx.origin_account_id == account_id)
        total_in = sum(tx.amount_kes for tx, _ in rows if tx.vendor_hash == account_id)
        flagged_cnt = sum(1 for tx, _ in rows if tx.verdict == 1)
        counterparties = set()
        history = []
        for tx, log in rows:
            role = "SENDER" if tx.origin_account_id == account_id else "RECIPIENT"
            cp = tx.vendor_hash if role == "SENDER" else tx.origin_account_id
            counterparties.add(cp)
            history.append(
                {
                    "tx_id": tx.tx_id,
                    "role": role,
                    "counterparty": cp,
                    "tx_type": tx.tx_type or "PAYMENT",
                    "amount_kes": tx.amount_kes,
                    "timestamp": tx.timestamp.isoformat() if tx.timestamp else None,
                    "verdict": tx.verdict,
                    "score": tx.score,
                    "action_taken": log.action_taken if log else "ALLOW",
                    "review_status": log.review_status if log else "PENDING",
                }
            )
        return {
            "account_id": account_id,
            "total_transactions": len(rows),
            "flagged_count": flagged_cnt,
            "total_outbound_kes": round(total_out, 2),
            "total_inbound_kes": round(total_in, 2),
            "unique_counterparties": len(counterparties),
            "transactions": history,
        }
    finally:
        session.close()


@app.get("/export/csv")
def export_csv():
    session = SessionLocal()
    try:
        rows = (
            session.query(Transaction, InferenceLog)
            .outerjoin(InferenceLog, Transaction.tx_id == InferenceLog.tx_id)
            .order_by(Transaction.timestamp.desc())
            .all()
        )
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow([
            "tx_id",
            "timestamp",
            "tx_type",
            "origin_account_id",
            "vendor_hash",
            "amount_kes",
            "oldbalance_org",
            "newbalance_orig",
            "score",
            "ml_score",
            "policy_score",
            "scoring_source",
            "verdict",
            "static_rule_verdict",
            "action_taken",
            "latency_ms",
            "review_status",
            "signals",
        ])
        for tx, log in rows:
            writer.writerow([
                tx.tx_id,
                tx.timestamp.isoformat() if tx.timestamp else "",
                tx.tx_type or "PAYMENT",
                tx.origin_account_id,
                tx.vendor_hash,
                tx.amount_kes,
                tx.oldbalance_org,
                tx.newbalance_orig,
                tx.score,
                log.ml_score if log else tx.score,
                log.policy_score if log else 0.0,
                log.scoring_source if log else "",
                tx.verdict,
                log.static_rule_verdict if log else 0,
                log.action_taken if log else "",
                log.latency_ms if log else 0.0,
                log.review_status if log else "PENDING",
                log.triggering_features if log else "[]",
            ])
        buf.seek(0)
        return StreamingResponse(
            iter([buf.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=anomaly_guard_audit_log.csv"},
        )
    finally:
        session.close()


@app.get("/metrics")
def model_metrics():
    if METRICS_PATH.exists():
        try:
            return json.loads(METRICS_PATH.read_text())
        except Exception:
            pass
    return {
        "available": False,
        "message": "Run train.py to generate model_metrics.json benchmark comparison.",
        "active_model": type(MODEL).__name__ if MODEL is not None else "Fallback",
        "threshold": THRESHOLD,
    }


@app.delete("/admin/logs")
def clear_logs(x_admin_token: Optional[str] = Header(default=None)):
    verify_admin_pin(x_admin_token)
    reset_db()
    return {"status": "cleared"}
