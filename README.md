# Anomaly Guard

Real-time B2B mobile money fraud detection API and Risk Operations Console tailored for Kenyan SACCOs, micro-lenders, and fintech payment gateways.

**Live Deployment:** https://anomaly-guard-api.onrender.com  
**Interactive API Docs:** https://anomaly-guard-api.onrender.com/docs

---

## Architecture

Legacy Kenyan mobile money controls rely on rigid static limits (e.g., flagging transactions over KES 50,000), which generate excessive false alarms on legitimate commerce while missing structuring ("smurfing") bursts, coordinated mule-ring fan-ins, and ledger-reconciliation tampering.

**Anomaly Guard** combines a calibrated ML classifier with deterministic behavioral and ledger-integrity guardrails:

* **FastAPI Scoring Engine (`main.py`):** Asynchronous REST gateway (`POST /score`) with idempotent transaction handling, transparent dual-score explainability (`ml_score` + `policy_score`), tiered policy recommendations, and `X-Admin-Token` / optional `X-API-Key` authentication.
* **XGBoost Classifier (`train.py`, `model.joblib`):** Trained on a strict 3-way temporal split of PaySim mobile money telemetry (Steps 1–500 Train, Steps 501–600 Validation, Steps 601–744 Unseen Holdout) with aligned training-serving velocity and account-drain features.
* **Velocity, Syndicate & Ledger Guardrails (`features.py`):** Computes rolling 15-minute and 24-hour sender velocity (smurfing detection), multi-sender destination fan-in (money-mule syndicate detection), ghost-hour drains, and sender/receiver balance reconciliation.
* **Normalized SQLite Audit Store (`database.py`):** WAL-mode SQLite schema linking `parsed_transactions` (1:1) to `ml_inference_log` (scores, latency, triggering signals, static-rule comparison, and SOC analyst dispositions) plus persisted `system_settings`.
* **4-Mode Risk Console (`dashboard.py`):** **Demo Mode** (6 Kenyan fraud scenarios), **Guided Mode** (8-step interactive schema onboarding), **Manual Mode** (developer/analyst payload testing), and **SLA & Benchmarks** (live 20-request concurrent load tester & model metrics).

---

## Verified Benchmarks

### 1. Unseen Temporal Holdout Evaluation (PaySim Steps 601–744 | 21,600 Transactions, 1,600 Fraud)

| Model / Baseline | Fraud F1 | Precision | Recall | False Positive Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Anomaly Guard XGBoost (cutoff = 0.20)** | **0.9975** | **99.87%** | **99.62%** | **0.01%** |
| Isolation Forest (Unsupervised Baseline) | 0.6335 | 65.47% | 61.38% | 2.59% |
| Legacy Static Rule (> KES 50,000) | 0.2309 | 13.28% | 88.50% | 46.24% |

*Note: High F1 on PaySim reflects the synthetic generator's deterministic balance-drain signature during fraud; production deployment requires retraining on live institution telemetry under ODPC compliance.*

### 2. Live Production Concurrency & Latency SLA (Render Free Tier)

Verified via `python simulator.py --url https://anomaly-guard-api.onrender.com --count 25 --concurrency 5`:

| Metric | Measured Result | SLA Target |
| :--- | :--- | :--- |
| Request Success Rate | **25 / 25 (100%)** | 100% |
| Server Inference Latency (Avg / p95) | **15.45 ms / 53.06 ms** | ≤ 1,500 ms |
| End-to-End Client RTT — Nairobi ↔ Render (Avg / p95 / Max) | **622.7 ms / 697.1 ms / 1,148.8 ms** | ≤ 1,500 ms (PASS) |

---

## Core API Endpoints

| Method | Endpoint | Purpose |
| :--- | :--- | :--- |
| `POST` | `/score` | Score a transaction in real time, compute SQLite velocity/fan-in, and persist audit log |
| `GET` | `/stats` | Aggregate KPIs, latency percentiles (avg/p95/max), SLA compliance, and static-rule delta |
| `GET` | `/transactions` | Paginated SQLite audit ledger joined with inference metadata and case status |
| `GET` | `/accounts/{account_id}` | Account investigation timeline across outbound and inbound counterparties |
| `PATCH` | `/logs/{tx_id}/disposition` | SOC analyst case disposition (`CONFIRMED_FRAUD` / `FALSE_POSITIVE` / `PENDING`) |
| `POST` | `/settings/threshold` | Persist SOC decision threshold (protected by `X-Admin-Token`) |
| `GET` | `/metrics` | Offline temporal holdout validation metrics (`model_metrics.json`) |
| `GET` | `/export/csv` | Download full SQLite inference audit trail as CSV |
| `DELETE` | `/admin/logs` | Clear demo audit logs (protected by `X-Admin-Token`) |

---

## Local Setup & Testing

    python3.11 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    # Run automated test suite (14 tests covering velocity, idempotency, tampering, fan-in, RBAC)
    python -m pytest -v

    # Start local API + Console
    uvicorn main:app --host 127.0.0.1 --port 8000

    # Run concurrent load test against local or remote instance
    python simulator.py --url http://127.0.0.1:8000 --count 30 --concurrency 5

## Privacy & Regulatory Compliance

This prototype strictly processes synthetic KES-adapted PaySim telemetry and pseudonymised identifiers (`KE_ACC_*`, `TILL_*`) in alignment with the **Kenya Data Protection Act (2019)**. No live M-Pesa, Airtel Money, or personal customer records are ingested.
