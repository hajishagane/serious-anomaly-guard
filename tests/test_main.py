import unittest
import unittest
import os
os.environ["TESTING"] = "true"
from fastapi.testclient import TestClient
from main import app
from database import init_db

class TestMainAPI(unittest.TestCase):
    def setUp(self):
        init_db()
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "ok")
        self.assertIn("model_loaded", data)

    def test_score_endpoint(self):
        payload = {
            "tx_id": "test-tx-001",
            "origin_account_id": "C99999",
            "vendor_hash": "M88888",
            "amount_kes": 1500.0,
            "timestamp": "2026-01-01T10:00:00"
        }
        response = self.client.post("/score", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["tx_id"], "test-tx-001")
        self.assertIn("verdict", data)
        self.assertIn("score", data)

    def test_score_idempotency(self):
        payload = {
            "tx_id": "test-idempotent",
            "origin_account_id": "C99999",
            "vendor_hash": "M88888",
            "amount_kes": 1500.0,
            "timestamp": "2026-01-01T10:00:00"
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
        self.client.post("/score", json={
            "tx_id": "ui-tx-1", "origin_account_id": "C1",
            "vendor_hash": "M1", "amount_kes": 500.0,
            "timestamp": "2026-01-01T12:00:00",
        })
        stats = self.client.get("/stats").json()
        self.assertEqual(stats["total_scored"], 1)
        txs = self.client.get("/transactions").json()
        self.assertEqual(len(txs["transactions"]), 1)
        self.assertEqual(txs["transactions"][0]["tx_id"], "ui-tx-1")

if __name__ == "__main__":
    unittest.main()
