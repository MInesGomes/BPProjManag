import unittest
from datetime import datetime, date, timedelta
from unittest.mock import MagicMock, patch
import pandas as pd

from proj_management_logic import (
    default_allocations_df,
    default_capacities,
    default_projects_df,
    default_requests_df,
    default_engineers,
    default_departments,
    default_eng_dept_map,
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


class TestSessionStateInitialization(unittest.TestCase):
    """Test suite for Streamlit session state initialization."""

    def setUp(self):
        """Set up mock session state before each test."""
        self.mock_session_state = {}

    def initialize_session_state(self):
        """
        Simulate the session state initialization logic from ProjManagement.py.
        Uses proj_management_logic functions to populate state.
        """
        base_date = datetime.today() - timedelta(days=datetime.today().weekday())
        
        if 'engineers_list' not in self.mock_session_state:
            self.mock_session_state['engineers_list'] = default_engineers()
            self.mock_session_state['departments_list'] = default_departments()
            self.mock_session_state['capacities'] = default_capacities()
            self.mock_session_state['eng_dept_map'] = default_eng_dept_map()

        if 'projects_df' not in self.mock_session_state:
            self.mock_session_state['projects_df'] = default_projects_df(base_date=base_date)

        if 'requests' not in self.mock_session_state:
            self.mock_session_state['requests'] = default_requests_df(base_date=base_date)
            self.mock_session_state['next_req_id'] = 1002

        if 'allocations' not in self.mock_session_state:
            self.mock_session_state['allocations'] = default_allocations_df()

    def test_session_state_engineers_list_initialized(self):
        """Test that engineers_list is initialized with 15 engineers."""
        self.initialize_session_state()
        
        self.assertIn('engineers_list', self.mock_session_state)
        self.assertEqual(len(self.mock_session_state['engineers_list']), 15)
        self.assertEqual(self.mock_session_state['engineers_list'][0], 'Engineer 1')
        self.assertEqual(self.mock_session_state['engineers_list'][-1], 'Engineer 15')

    def test_session_state_departments_list_initialized(self):
        """Test that departments_list is initialized with correct departments."""
        self.initialize_session_state()
        
        self.assertIn('departments_list', self.mock_session_state)
        expected_depts = ["Backend", "Frontend", "DevOps", "QA", "Data Science"]
        self.assertEqual(self.mock_session_state['departments_list'], expected_depts)

    def test_session_state_capacities_initialized(self):
        """Test that capacities dictionary is initialized correctly."""
        self.initialize_session_state()
        
        self.assertIn('capacities', self.mock_session_state)
        capacities = self.mock_session_state['capacities']
        self.assertEqual(len(capacities), 15)
        # Check the weekly capacity rule: divisible by 3 get 32, others get 40
        self.assertEqual(capacities['Engineer 3'], 32)
        self.assertEqual(capacities['Engineer 1'], 40)

    def test_session_state_eng_dept_map_initialized(self):
        """Test that engineer-to-department mapping is initialized."""
        self.initialize_session_state()
        
        self.assertIn('eng_dept_map', self.mock_session_state)
        eng_dept_map = self.mock_session_state['eng_dept_map']
        self.assertEqual(len(eng_dept_map), 15)
        # Check that all engineers are mapped to valid departments
        for eng, dept in eng_dept_map.items():
            self.assertIn(dept, self.mock_session_state['departments_list'])

    def test_session_state_projects_df_initialized(self):
        """Test that projects DataFrame is initialized."""
        self.initialize_session_state()
        
        self.assertIn('projects_df', self.mock_session_state)
        projects_df = self.mock_session_state['projects_df']
        self.assertIsInstance(projects_df, pd.DataFrame)
        self.assertEqual(len(projects_df), 5)
        self.assertEqual(list(projects_df.columns), ["Project", "Proj Start", "Proj End"])

    def test_session_state_requests_initialized(self):
        """Test that requests DataFrame is initialized with pending request."""
        self.initialize_session_state()
        
        self.assertIn('requests', self.mock_session_state)
        requests_df = self.mock_session_state['requests']
        self.assertIsInstance(requests_df, pd.DataFrame)
        self.assertEqual(len(requests_df), 1)
        self.assertEqual(requests_df.loc[0, 'Status'], 'Pending')
        self.assertEqual(requests_df.loc[0, 'Req ID'], 1001)

    def test_session_state_next_req_id_initialized(self):
        """Test that next_req_id counter is initialized."""
        self.initialize_session_state()
        
        self.assertIn('next_req_id', self.mock_session_state)
        self.assertEqual(self.mock_session_state['next_req_id'], 1002)

    def test_session_state_allocations_initialized(self):
        """Test that allocations DataFrame is initialized as empty."""
        self.initialize_session_state()
        
        self.assertIn('allocations', self.mock_session_state)
        allocations_df = self.mock_session_state['allocations']
        self.assertIsInstance(allocations_df, pd.DataFrame)
        self.assertTrue(allocations_df.empty)
        expected_cols = [
            "Engineer", "Department", "Project", "Start Date", 
            "End Date", "Hours/Day", "Linked Req ID"
        ]
        self.assertEqual(list(allocations_df.columns), expected_cols)

    def test_all_required_session_state_keys_present(self):
        """Test that all required session state keys are initialized."""
        self.initialize_session_state()
        
        required_keys = [
            'engineers_list', 'departments_list', 'capacities', 'eng_dept_map',
            'projects_df', 'requests', 'next_req_id', 'allocations'
        ]
        
        for key in required_keys:
            self.assertIn(key, self.mock_session_state, 
                         f"Session state missing required key: {key}")

    def test_session_state_idempotent(self):
        """Test that calling initialize_session_state multiple times is idempotent."""
        self.initialize_session_state()
        first_state = {k: v for k, v in self.mock_session_state.items()}
        
        # Initialize again
        self.initialize_session_state()
        second_state = self.mock_session_state
        
        # Verify keys are the same
        self.assertEqual(set(first_state.keys()), set(second_state.keys()))


if __name__ == "__main__":
    unittest.main()
