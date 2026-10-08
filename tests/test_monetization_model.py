import unittest

from src.monetization_model import Assumptions, calculate, sensitivity


class MonetizationModelTest(unittest.TestCase):
    def test_base_case(self):
        result = calculate(Assumptions())
        self.assertAlmostEqual(result["cost_per_job_vnd"], 2759.6033, places=3)
        self.assertAlmostEqual(result["floor_vnd_per_job"], 8278.8098, places=3)
        self.assertAlmostEqual(result["monthly_revenue_vnd"], 3_590_000)
        self.assertAlmostEqual(result["gross_margin"], 0.723271, places=6)
        self.assertAlmostEqual(result["breakeven_completion_60gm"], 0.637898, places=6)

    def test_denominator_is_completed_jobs(self):
        a = Assumptions(completion_rate=0.50)
        result = calculate(a)
        self.assertAlmostEqual(result["completed_jobs"], 500)
        self.assertAlmostEqual(
            result["cost_per_job_usd"], result["cost_per_attempt_usd"] / 0.50
        )

    def test_sensitivity_monotonic(self):
        rows = sensitivity(Assumptions())
        costs = [row["cost_per_job_vnd"] for row in rows]
        margins = [row["gross_margin"] for row in rows]
        self.assertEqual(costs, sorted(costs, reverse=True))
        self.assertEqual(margins, sorted(margins))

    def test_invalid_rate(self):
        with self.assertRaises(ValueError):
            calculate(Assumptions(completion_rate=0))


if __name__ == "__main__":
    unittest.main()

