import unittest
from datetime import datetime, date, timedelta
import pandas as pd

from proj_management_logic import (
    default_allocations_df,
    default_capacities,
    default_projects_df,
    default_requests_df,
    get_daily_load,
)

class TestProjManagementLogic(unittest.TestCase):
    def test_default_projects_df_has_expected_columns(self):
        base_date = datetime(2026, 1, 5)
        projects_df = default_projects_df(base_date=base_date)

        self.assertEqual(list(projects_df.columns), ["Project", "Proj Start", "Proj End"])
        self.assertEqual(len(projects_df), 5)
        self.assertEqual(projects_df.loc[0, "Proj Start"], date(2026, 1, 5))
        self.assertEqual(projects_df.loc[0, "Proj End"], date(2026, 3, 6))

    def test_default_requests_df_contains_pending_request(self):
        base_date = datetime(2026, 1, 5)
        requests_df = default_requests_df(base_date=base_date)

        self.assertEqual(len(requests_df), 1)
        self.assertEqual(requests_df.loc[0, "Req ID"], 1001)
        self.assertEqual(requests_df.loc[0, "Status"], "Pending")
        self.assertEqual(requests_df.loc[0, "Start Date"], date(2026, 1, 5))

    def test_default_allocations_df_has_expected_columns(self):
        allocations_df = default_allocations_df()

        self.assertEqual(
            list(allocations_df.columns),
            [
                "Engineer",
                "Department",
                "Project",
                "Start Date",
                "End Date",
                "Hours/Day",
                "Linked Req ID",
            ],
        )
        self.assertTrue(allocations_df.empty)

    def test_default_capacities_applies_weekly_cap_rule(self):
        capacities = default_capacities()

        self.assertEqual(capacities["Engineer 3"], 32)
        self.assertEqual(capacities["Engineer 4"], 40)

    def test_get_daily_load_returns_zero_for_empty_allocations(self):
        allocations_df = default_allocations_df()
        start_date = date(2026, 1, 6)
        end_date = date(2026, 1, 9)

        daily_load = get_daily_load(allocations_df, "Engineer 1", start_date, end_date)
        expected = {
            date(2026, 1, 6): 0,
            date(2026, 1, 7): 0,
            date(2026, 1, 8): 0,
            date(2026, 1, 9): 0,
        }
        self.assertEqual(daily_load, expected)

    def test_get_daily_load_accumulates_hours_for_overlapping_allocation(self):
        allocations_df = pd.DataFrame(
            [
                {
                    "Engineer": "Engineer 1",
                    "Department": "QA",
                    "Project": "Project Alpha",
                    "Start Date": date(2026, 1, 7),
                    "End Date": date(2026, 1, 9),
                    "Hours/Day": 4,
                    "Linked Req ID": 1001,
                }
            ]
        )

        start_date = date(2026, 1, 6)
        end_date = date(2026, 1, 9)

        daily_load = get_daily_load(allocations_df, "Engineer 1", start_date, end_date)
        expected = {
            date(2026, 1, 6): 0,
            date(2026, 1, 7): 4,
            date(2026, 1, 8): 4,
            date(2026, 1, 9): 4,
        }
        self.assertEqual(daily_load, expected)


if __name__ == "__main__":
    unittest.main()
