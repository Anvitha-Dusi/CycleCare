"""
test_app.py
-------------------------------------------------------------------------------
Automated test suite verifying CycleCare API endpoints, auth, CRUD operations,
and cycle estimation logic.
-------------------------------------------------------------------------------
"""

import unittest
from datetime import date, timedelta
from app import app
from database.db import init_db


class CycleCareTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with app.app_context():
            init_db()
            from database.db import execute_db
            execute_db("DELETE FROM users WHERE email = %s", ("maya@example.com",))

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_01_registration_and_validation(self):
        # Missing fields
        res = self.client.post("/api/register", json={
            "name": "",
            "email": "invalid-email",
            "password": "123",
            "confirm_password": "456"
        })
        self.assertEqual(res.status_code, 400)

        # Successful registration
        res = self.client.post("/api/register", json={
            "name": "Maya Lin",
            "email": "maya@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["user"]["name"], "Maya Lin")

        # Duplicate email
        res = self.client.post("/api/register", json={
            "name": "Maya Duplicate",
            "email": "maya@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        self.assertEqual(res.status_code, 400)

    def test_02_login_and_logout(self):
        # Invalid credentials
        res = self.client.post("/api/login", json={
            "email": "maya@example.com",
            "password": "wrongpassword"
        })
        self.assertEqual(res.status_code, 401)

        # Valid login
        res = self.client.post("/api/login", json={
            "email": "maya@example.com",
            "password": "password123"
        })
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.get_json()["success"])

        # Check me
        res = self.client.get("/api/me")
        self.assertEqual(res.status_code, 200)

        # Logout
        res = self.client.post("/api/logout")
        self.assertEqual(res.status_code, 200)

        # Me after logout should be 401
        res = self.client.get("/api/me")
        self.assertEqual(res.status_code, 401)

    def test_03_cycle_crud_and_estimation(self):
        # Log in as Maya
        self.client.post("/api/login", json={
            "email": "maya@example.com",
            "password": "password123"
        })

        # CREATE: Add first cycle (e.g. 2026-09-01, duration 5 days, length 28 days)
        res = self.client.post("/api/cycles", json={
            "start_date": "2026-09-01",
            "period_duration": 5,
            "cycle_length": 28,
            "notes": "Mild cramps on day 1"
        })
        self.assertEqual(res.status_code, 201)
        cycle1 = res.get_json()["cycle"]
        cycle1_id = cycle1["id"]

        # CREATE: Add second cycle (e.g. 2026-09-29, duration 5 days, length 28 days)
        res = self.client.post("/api/cycles", json={
            "start_date": "2026-09-29",
            "period_duration": 5,
            "cycle_length": 28,
            "notes": "Regular flow"
        })
        self.assertEqual(res.status_code, 201)
        cycle2_id = res.get_json()["cycle"]["id"]

        # READ (List)
        res = self.client.get("/api/cycles")
        self.assertEqual(res.status_code, 200)
        cycles = res.get_json()["cycles"]
        self.assertGreaterEqual(len(cycles), 2)

        # READ (Single)
        res = self.client.get(f"/api/cycles/{cycle1_id}")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["cycle"]["notes"], "Mild cramps on day 1")

        # UPDATE: Update cycle 1 notes and length
        res = self.client.put(f"/api/cycles/{cycle1_id}", json={
            "start_date": "2026-09-01",
            "end_date": "2026-09-05",
            "period_duration": 5,
            "cycle_length": 29,
            "notes": "Updated notes: rested well"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["cycle"]["notes"], "Updated notes: rested well")

        # DASHBOARD: Verify estimation
        res = self.client.get("/api/dashboard")
        self.assertEqual(res.status_code, 200)
        dash = res.get_json()
        self.assertTrue(dash["has_data"])
        self.assertIn("Estimated Next Period", dash["formula_explanation"])
        self.assertIsNotNone(dash["estimated_next_period"])

        # DELETE: Delete cycle 1
        res = self.client.delete(f"/api/cycles/{cycle1_id}")
        self.assertEqual(res.status_code, 200)

        # Verify deletion
        res = self.client.get(f"/api/cycles/{cycle1_id}")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
