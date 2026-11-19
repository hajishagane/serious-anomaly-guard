import os
import unittest

os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from database import reset_db
from main import app


class TestMainAPI(unittest.TestCase):
    def setUp(self):
        reset_db()
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("model_loaded", data)
        self.assertIn("threshold", data)

    def test_score_endpoint(self):
        payload = {
            "tx_id": "test-tx-001",
            "origin_account_id": "C99999",
            "vendor_hash": "M88888",
            "amount_kes": 1500.0,
            "timestamp": "2026-01-01T10:00:00",
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tx_id"], "test-tx-001")
        self.assertIn("verdict", data)
        self.assertIn("score", data)
        self.assertIn("ml_score", data)
        self.assertIn("policy_score", data)
        self.assertIn("static_rule_verdict", data)
        self.assertLess(data["latency_ms"], 1500.0)

    def test_score_idempotency(self):
        payload = {
            "tx_id": "test-idempotent",
            "origin_account_id": "C99999",
            "vendor_hash": "M88888",
            "amount_kes": 1500.0,
            "timestamp": "2026-01-01T10:00:00",
        }
        res1 = self.client.post("/score", json=payload)
        self.assertEqual(res1.status_code, 200)

        res2 = self.client.post("/score", json=payload)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res1.json(), res2.json())

    def test_dashboard_ui(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers["content-type"])
        self.assertIn("Anomaly", response.text)

    def test_stats_and_transactions(self):
        self.client.post(
            "/score",
            json={
                "tx_id": "ui-tx-1",
                "origin_account_id": "C1",
                "vendor_hash": "M1",
                "amount_kes": 500.0,
                "timestamp": "2026-01-01T12:00:00",
                "oldbalance_org": 5000.0,
                "newbalance_orig": 4500.0,
                "newbalance_dest": 10500.0,
            },
        )
        stats = self.client.get("/stats").json()
        self.assertEqual(stats["total_scored"], 1)
        txs = self.client.get("/transactions").json()
        self.assertEqual(len(txs["transactions"]), 1)
        self.assertEqual(txs["transactions"][0]["tx_id"], "ui-tx-1")

    def test_ledger_reconciliation_mismatch_flagged(self):
        res = self.client.post(
            "/score",
            json={
                "tx_id": "tx-tamper-1",
                "tx_type": "PAYMENT",
                "origin_account_id": "KE_ACC_101",
                "vendor_hash": "TILL_55",
                "amount_kes": 2500.0,
                "oldbalance_org": 12500.0,
                "newbalance_orig": 11000.0,
                "newbalance_dest": 25000.0,
                "timestamp": "2026-06-15T14:00:00",
            },
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["verdict"], 1)
        self.assertEqual(data["static_rule_verdict"], 0)
        self.assertTrue(any("ledger mismatch" in s.lower() for s in data["signals"]))

    def test_smurfing_burst_beats_static_rule(self):
        bal = 5400.0
        last_data = None
        for i in range(6):
            res = self.client.post(
                "/score",
                json={
                    "tx_id": f"smurf-{i}",
                    "tx_type": "TRANSFER",
                    "origin_account_id": "KE_SMURF_TEST",
                    "vendor_hash": f"PROXY_{i}",
                    "amount_kes": 900.0,
                    "oldbalance_org": bal,
                    "newbalance_orig": bal - 900.0,
                    "newbalance_dest": 0.0,
                    "timestamp": f"2026-06-15T14:0{i}:00",
                },
            )
            self.assertEqual(res.status_code, 200)
            last_data = res.json()
            bal -= 900.0
        self.assertEqual(last_data["verdict"], 1)
        self.assertEqual(last_data["static_rule_verdict"], 0)
        self.assertGreaterEqual(last_data["features"]["tx_count_15min"], 3)

    def test_mule_ring_fan_in_syndicate(self):
        last_data = None
        for i, sender in enumerate(["KE_VICTIM_1", "KE_VICTIM_2", "KE_VICTIM_3"]):
            res = self.client.post(
                "/score",
                json={
                    "tx_id": f"mule-fanin-{i}",
                    "tx_type": "TRANSFER",
                    "origin_account_id": sender,
                    "vendor_hash": "SYNDICATE_MULE_777",
                    "amount_kes": 18000.0,
                    "oldbalance_org": 25000.0,
                    "newbalance_orig": 7000.0,
                    "newbalance_dest": 18000.0 * (i + 1),
                    "timestamp": f"2026-06-15T15:0{i}:00",
                },
            )
            self.assertEqual(res.status_code, 200)
            last_data = res.json()
        self.assertEqual(last_data["verdict"], 1)
        self.assertEqual(last_data["static_rule_verdict"], 0)
        self.assertGreaterEqual(last_data["features"]["vendor_unique_senders_15min"], 2)

    def test_soc_admin_auth_and_case_workflow(self):
        bad = self.client.post(
            "/settings/threshold",
            json={"threshold": 0.65},
            headers={"X-Admin-Token": "wrong"},
        )
        self.assertEqual(bad.status_code, 401)

        good = self.client.post(
            "/settings/threshold",
            json={"threshold": 0.70},
            headers={"X-Admin-Token": "2026"},
        )
        self.assertEqual(good.status_code, 200)
        self.assertEqual(good.json()["threshold"], 0.70)

        # Reset threshold back to 0.80
        self.client.post(
            "/settings/threshold",
            json={"threshold": 0.80},
            headers={"X-Admin-Token": "2026"},
        )

        # Test analyst disposition, account timeline, and CSV export
        self.client.post(
            "/score",
            json={
                "tx_id": "case-tx-1",
                "tx_type": "CASH_OUT",
                "origin_account_id": "KE_CASE_ACCT",
                "vendor_hash": "AGENT_09",
                "amount_kes": 185000.0,
                "oldbalance_org": 185000.0,
                "newbalance_orig": 0.0,
                "newbalance_dest": 0.0,
                "timestamp": "2026-06-15T02:30:00",
            },
        )
        disp = self.client.patch(
            "/logs/case-tx-1/disposition",
            json={"review_status": "CONFIRMED_FRAUD"},
        )
        self.assertEqual(disp.status_code, 200)
        self.assertEqual(disp.json()["review_status"], "CONFIRMED_FRAUD")

        acct = self.client.get("/accounts/KE_CASE_ACCT")
        self.assertEqual(acct.status_code, 200)
        self.assertEqual(acct.json()["flagged_count"], 1)

        csv_res = self.client.get("/export/csv")
        self.assertEqual(csv_res.status_code, 200)
        self.assertIn("case-tx-1", csv_res.text)
        self.assertIn("CONFIRMED_FRAUD", csv_res.text)


if __name__ == "__main__":
    unittest.main()
