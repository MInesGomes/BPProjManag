import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional


def default_engineers() -> List[str]:
    return [f"Engineer {i}" for i in range(1, 16)]


def default_departments() -> List[str]:
    return ["Backend", "Frontend", "DevOps", "QA", "Data Science"]


def default_capacities(engineers: Optional[List[str]] = None) -> Dict[str, int]:
    if engineers is None:
        engineers = default_engineers()
    return {eng: (32 if int(eng.split()[1]) % 3 == 0 else 40) for eng in engineers}


def default_eng_dept_map(
    engineers: Optional[List[str]] = None,
    departments: Optional[List[str]] = None,
) -> Dict[str, str]:
    if engineers is None:
        engineers = default_engineers()
    if departments is None:
        departments = default_departments()

    return {eng: departments[i % len(departments)] for i, eng in enumerate(engineers)}


def default_projects_df(base_date: Optional[datetime] = None) -> pd.DataFrame:
    if base_date is None:
        base_date = datetime.today() - timedelta(days=datetime.today().weekday())

    project_names = [
        "Project Alpha",
        "Project Beta",
        "Project Gamma",
        "Project Delta",
        "Project Epsilon",
    ]

    projects_data = []
    for idx, p_name in enumerate(project_names):
        start_dt = base_date + timedelta(days=idx * 7)
        end_dt = start_dt + timedelta(days=60)
        projects_data.append(
            {
                "Project": p_name,
                "Proj Start": start_dt.date(),
                "Proj End": end_dt.date(),
            }
        )

    return pd.DataFrame(projects_data)


def default_requests_df(base_date: Optional[datetime] = None) -> pd.DataFrame:
    if base_date is None:
        base_date = datetime.today() - timedelta(days=datetime.today().weekday())

    return pd.DataFrame(
        [
            {
                "Req ID": 1001,
                "Project": "Project Alpha",
                "Required Dept": "QA",
                "Start Date": base_date.date(),
                "End Date": (base_date + timedelta(days=14)).date(),
                "Hours/Day": 4,
                "Status": "Pending",
                "Assigned Engineer": "None",
            }
        ]
    )


def default_allocations_df() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "Engineer",
            "Department",
            "Project",
            "Start Date",
            "End Date",
            "Hours/Day",
            "Linked Req ID",
        ]
    )


def get_daily_load(
    allocations_df: pd.DataFrame,
    target_eng: str,
    start_date,
    end_date,
) -> Dict[datetime.date, int]:
    if allocations_df is None or allocations_df.empty:
        dates = pd.date_range(start=start_date, end=end_date, freq="B")
        return {d.date(): 0 for d in dates}

    eng_allocs = allocations_df[allocations_df["Engineer"] == target_eng]
    dates = pd.date_range(start=start_date, end=end_date, freq="B")
    daily_hours = {d.date(): 0 for d in dates}

    for _, row in eng_allocs.iterrows():
        overlap_dates = pd.date_range(
            start=max(start_date, row["Start Date"]),
            end=min(end_date, row["End Date"]),
            freq="B",
        )
        for ed in overlap_dates:
            if ed.date() in daily_hours:
                daily_hours[ed.date()] += row["Hours/Day"]

    return daily_hours
