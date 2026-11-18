import os, json, csv, io
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import httpx
import streamlit as st

st.set_page_config(page_title="Anomaly Guard", layout="wide")

# ── helpers ──────────────────────────────────────────────────────────
BASE = os.getenv("API_BASE", "http://localhost:7860")
TOKEN = os.getenv("API_TOKEN", "")

def api(path, method="GET", json=None, headers=None):
    h = {"Content-Type": "application/json"}
    if headers: h.update(headers)
    url = f"{BASE}{path}"
    r = httpx.request(method, url, headers=h, json=json, timeout=15)
    r.raise_for_status()
    return r.json()

# ── UI ────────────────────────────────────────────────────────────────
st.title("🛡️ Anomaly Guard — Live Scoring")
st.caption("XGBoost fraud scoring · see recent transactions · /docs for API")

with st.sidebar:
    st.markdown("**Endpoint**")
    api_url = st.text_input("API base URL", value=BASE, help="e.g. https://my-app-xyz.hf.space")
    st.markdown("---")
    if st.button("Refresh stats"):
        st.rerun()

# split layout
left, right = st.columns([2, 1])

# ── recent transactions ─────────────────────────────────────────────
with right:
    st.subheader("Recent scored transactions")
    if st.button("Load latest 20"):
        try:
            data = api("/transactions?limit=20", headers={"X-API-Token": TOKEN})
            rows = data.get("transactions", [])
            if rows:
                st.dataframe(
                    pd.DataFrame(rows,
                        columns=["tx_id","origin_account_id","amount_kes",
                                 "timestamp","score","verdict"]),
                    hide_index=True, column_config={
                        "score": st.column_config.ProgressColumn(
                            "score %", min_value=0, max_value=100),
                        "verdict": st.column_config.SelectboxColumn(
                            "verdict", options=["FRAUD", "LEGIT"])
                    }
                )
            else:
                st.info("No transactions yet")
        except Exception as e:
            st.error(f"Could not load transactions: {e}")

# ── score form ──────────────────────────────────────────────────────
with left:
    st.subheader("Score a new transaction")
    with st.form("score_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            tx_id = st.text_input("Tx ID", value=f"ui-{datetime.now():%Y%m%d%H%M%S}")
            orig = st.text_input("Origin account", value="C1001")
            vend = st.text_input("Vendor hash", value="M2001")
        with c2:
            amt = st.number_input("Amount (KES)", min_value=0.0, value=5000.0, step=100.0)
            ob = st.number_input("Old balance (orig)", min_value=0.0, value=10000.0, step=100.0)
            nb = st.number_input("New balance (orig)", min_value=0.0, value=5000.0, step=100.0)
        ts = st.text_input("Timestamp", value=datetime.now().strftime("%Y-%m-%dT%H:%M"))
        submitted = st.form_submit_button("Score transaction")

    if submitted:
        with st.spinner("Scoring…"):
            payload = {
                "tx_id": tx_id,
                "origin_account_id": orig,
                "vendor_hash": vend,
                "amount_kes": float(amt),
                "oldbalance_org": float(ob),
                "newbalance_orig": float(nb),
                "newbalance_dest": st.number_input("New balance (dest)", min_value=0.0, value=0.0, step=100.0),
                "timestamp": ts,
            }
            try:
                out = api("/score", method="POST", json=payload, headers={"X-API-Token": TOKEN})
                verdict = out.get("verdict")
                score = out.get("score", 0) * 100
                msg = (
                    f"⚠️ FRAUD ALERT — {score:.1f}% fraud probability"
                    if verdict == 1
                    else f"✅ Legitimate — {score:.1f}% fraud probability"
                )
                st.success(f"Tx **{out['tx_id']}**: {msg}")
                st.caption(f"Features: {json.dumps(out.get('features', {}), indent=2)}")
            except httpx.HTTPStatusError as e:
                st.error(f"API error: {e.response.status_code} {e.response.text}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

# ── health widget ───────────────────────────────────────────────────
with st.expander("Service health", expanded=False):
    if st.button("Check health"):
        try:
            j = api("/health")
            st.json(j)
        except Exception as e:
            st.error(f"Health check failed: {e}")

st.markdown("---")
st.caption("Data is ephemeral; SQLite lives only in the container's local storage.")