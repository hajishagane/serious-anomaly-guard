import argparse
import os
import random
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests


def build_synthetic_batch(count: int):
    now = datetime.now()
    batch = []
    smurf_acct = f"KE_SIM_SMURF_{random.randint(1000, 9999)}"
    smurf_bal = 5400.0
    mule_wallet = f"MULE_SIM_RING_{random.randint(100, 999)}"

    for i in range(count):
        if i % 10 in (2, 3, 4, 5):
            # Structuring / smurfing burst (below KES 50k static rule)
            amt = 900.0
            new_bal = max(0.0, smurf_bal - amt)
            payload = {
                "tx_id": f"sim-smurf-{uuid.uuid4().hex[:8]}",
                "tx_type": "TRANSFER",
                "origin_account_id": smurf_acct,
                "vendor_hash": f"PROXY_SIM_{i}",
                "amount_kes": amt,
                "timestamp": (now + timedelta(seconds=i * 10)).strftime("%Y-%m-%dT%H:%M:%S"),
                "oldbalance_org": smurf_bal,
                "newbalance_orig": new_bal,
                "newbalance_dest": 0.0,
            }
            smurf_bal = new_bal if new_bal >= 900 else 5400.0
        elif i % 10 in (7, 8, 9):
            # Coordinated mule-ring fan-in
            payload = {
                "tx_id": f"sim-ring-{uuid.uuid4().hex[:8]}",
                "tx_type": "TRANSFER",
                "origin_account_id": f"KE_SIM_VICTIM_{i}",
                "vendor_hash": mule_wallet,
                "amount_kes": 18000.0,
                "timestamp": (now + timedelta(seconds=i * 12)).strftime("%Y-%m-%dT%H:%M:%S"),
                "oldbalance_org": 25000.0,
                "newbalance_orig": 7000.0,
                "newbalance_dest": 18000.0 * (i + 1),
            }
        elif i % 10 == 6:
            # Ghost-hour SIM-swap drain
            ghost = now.replace(hour=2, minute=30, second=0)
            payload = {
                "tx_id": f"sim-drain-{uuid.uuid4().hex[:8]}",
                "tx_type": "CASH_OUT",
                "origin_account_id": f"KE_SIM_DRAIN_{i}",
                "vendor_hash": "AGENT_SIM_991",
                "amount_kes": 185000.0,
                "timestamp": ghost.strftime("%Y-%m-%dT%H:%M:%S"),
                "oldbalance_org": 185000.0,
                "newbalance_orig": 0.0,
                "newbalance_dest": 0.0,
            }
        else:
            # Normal Kenyan retail / P2P transaction
            amt = round(random.uniform(150.0, 4500.0), 2)
            old_b = round(amt + random.uniform(2000.0, 25000.0), 2)
            payload = {
                "tx_id": f"sim-norm-{uuid.uuid4().hex[:8]}",
                "tx_type": "PAYMENT",
                "origin_account_id": f"KE_SIM_USER_{random.randint(100, 999)}",
                "vendor_hash": random.choice(["TILL_NAIVAS_4021", "PAYBILL_KPLC_888880", "TILL_QUICKMART_305"]),
                "amount_kes": amt,
                "timestamp": (now + timedelta(seconds=i * 5)).strftime("%Y-%m-%dT%H:%M:%S"),
                "oldbalance_org": old_b,
                "newbalance_orig": round(old_b - amt, 2),
                "newbalance_dest": round(random.uniform(10000.0, 120000.0), 2),
            }
        batch.append(payload)
    return batch


def load_csv_batch(csv_path: str, limit: int):
    sim_df = pd.read_csv(csv_path).sort_values("step").head(limit).reset_index(drop=True)
    base_dt = datetime(2026, 1, 1, 0, 0, 0)
    batch = []
    for _, row in sim_df.iterrows():
        ts = base_dt + timedelta(hours=int(row["step"]))
        batch.append({
            "tx_id": f"sim-{int(row['step'])}-{row.name}-{uuid.uuid4().hex[:4]}",
            "tx_type": str(row.get("type", "TRANSFER")),
            "origin_account_id": str(row["origin_account_id"]),
            "vendor_hash": str(row["vendor_hash"]),
            "amount_kes": float(row["amount_kes"]),
            "timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S"),
            "oldbalance_org": float(row.get("oldbalance_org", 0.0)),
            "newbalance_orig": float(row.get("newbalance_orig", 0.0)),
            "newbalance_dest": float(row.get("newbalance_dest", 0.0)),
        })
    return batch


def send_one(base_url: str, payload: dict, api_key: str = ""):
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-API-Key"] = api_key
    t0 = time.perf_counter()
    resp = requests.post(f"{base_url.rstrip('/')}/score", json=payload, headers=headers, timeout=30)
    rtt_ms = (time.perf_counter() - t0) * 1000.0
    return resp.status_code, rtt_ms, (resp.json() if resp.status_code == 200 else resp.text)


def main():
    parser = argparse.ArgumentParser(description="Anomaly Guard PaySim-KES Telemetry Simulator & Load Tester")
    parser.add_argument("--url", default=os.getenv("BASE_URL", "http://127.0.0.1:8000"), help="Target API base URL")
    parser.add_argument("--count", type=int, default=30, help="Number of transactions to dispatch")
    parser.add_argument("--concurrency", type=int, default=5, help="Concurrent worker threads")
    parser.add_argument("--csv", default="processed_sim.csv", help="Optional preprocessed PaySim CSV path")
    parser.add_argument("--api-key", default=os.getenv("API_KEY", ""), help="Optional X-API-Key header")
    args = parser.parse_args()

    if args.csv and os.path.exists(args.csv):
        print(f"Loading {args.count} PaySim records from {args.csv}...")
        batch = load_csv_batch(args.csv, args.count)
    else:
        print(f"Generating {args.count} synthetic PaySim-KES Kenyan telemetry records...")
        batch = build_synthetic_batch(args.count)

    print(f"Dispatching to {args.url}/score with concurrency={args.concurrency}...")
    t_wall = time.perf_counter()
    rtts, server_lats = [], []
    ok, flagged, static_missed = 0, 0, 0

    with ThreadPoolExecutor(max_workers=max(1, args.concurrency)) as pool:
        futures = [pool.submit(send_one, args.url, p, args.api_key) for p in batch]
        for fut in as_completed(futures):
            code, rtt, body = fut.result()
            if code == 200:
                ok += 1
                rtts.append(rtt)
                server_lats.append(float(body.get("latency_ms", 0.0)))
                if body.get("verdict") == 1:
                    flagged += 1
                    if body.get("static_rule_verdict") == 0:
                        static_missed += 1
            else:
                print(f"ERROR HTTP {code}: {body}")

    wall_s = time.perf_counter() - t_wall
    print("\n=== Anomaly Guard Load Test Summary ===")
    print(f"Success: {ok}/{len(batch)} | Throughput: {ok / max(wall_s, 0.001):.1f} req/s")
    print(f"Flagged: {flagged} (Caught beyond static KES 50k rule: {static_missed})")
    if rtts:
        print(f"Client RTT (ms)  -> min: {min(rtts):.1f} | avg: {np.mean(rtts):.1f} | p95: {np.percentile(rtts, 95):.1f} | max: {max(rtts):.1f}")
        print(f"Server Calc (ms) -> avg: {np.mean(server_lats):.2f} | p95: {np.percentile(server_lats, 95):.2f}")
        print(f"NFR-01 SLA (<1500ms): {'PASS' if np.percentile(rtts, 95) <= 1500 else 'FAIL'}")


if __name__ == "__main__":
    main()
