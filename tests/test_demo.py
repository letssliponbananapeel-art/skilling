# SPDX-License-Identifier: MPL-2.0
import json
from pathlib import Path
import unittest
from demo import discover, decide, balance

class DemoTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).resolve().parents[1] / "data/visual_composition.json").read_text())
        self.candidate = discover(self.data["events"])

    def test_fixture_counts_and_preference_exclusion(self):
        self.assertEqual((self.candidate["evidence"], self.candidate["successful"], self.candidate["confidence"]), (47,39,83))
        self.assertNotIn("Likes blue", self.candidate["frequent_signals"])
        self.assertEqual(sum(self.candidate["frequent_signals"].values()),47)

    def test_no_evidence_is_not_zero_confidence(self):
        self.assertIsNone(discover([])["confidence"])

    def test_acceptance_does_not_imply_success(self):
        event = {**self.data["events"][0], "action":"Accept", "outcome":"unknown"}
        self.assertEqual(discover([event])["successful"],0)

    def test_unconfirmed_candidates_do_not_assign_roles(self):
        for decision in ("observe", "reject"):
            self.assertEqual(balance(decide(self.candidate, decision),self.data["friction"])["ai"],[])

    def test_registration_and_friction_change_roles(self):
        c = decide(self.candidate,"register")
        self.assertEqual(len(balance(c,self.data["friction"])["ai"]),2)
        low = {**self.data["friction"], "task_frequency":"low", "user_stress":"low", "capability_gap":"none", "failure_cost":"low"}
        self.assertEqual(balance(c,low)["ai"],[])
        self.assertIn("small reversible",balance(c,low)["behavior"])

    def test_duplicate_evidence_rejected(self):
        with self.assertRaises(ValueError):
            discover([self.data["events"][0]]*2)

if __name__ == "__main__":
    unittest.main()
