# 🚀 ResSync — Resource Workflow Portal

**ResSync** is a Streamlit-based resource allocation and capacity planning tool that helps organizations schedule engineers across multiple projects while preventing overallocation and improving visibility into who's working on what.

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/streamlit-app-FF4B4B)
![License](https://img.shields.io/badge/status-in%20development-yellow)

---

## Table of Contents

- [Overview](#overview)
- [Business Problem](#business-problem)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Usage Guide](#usage-guide)
- [Running Tests](#running-tests)
- [Project Methodology](#project-methodology)

---

## Overview

ResSync addresses the challenges of managing shared engineering resources across multiple concurrent projects. It gives **Project Managers** a way to request resources and track status, and **Department Managers** a way to evaluate capacity, approve requests, and assign engineers — backed by real-time workload analysis and visualization.

## Business Problem

Organizations frequently share a limited pool of engineers across multiple projects. When this is managed through spreadsheets and manual communication, it tends to lead to:

- Resource overallocation
- Scheduling conflicts
- Limited visibility into engineer workloads
- Delayed project delivery
- Inefficient staffing decisions
- Difficulty tracking resource availability

As project complexity grows, manual resource planning becomes error-prone and hard to maintain.

## Key Features

### 📝 Resource Request Management
- Submit resource requests for a project, department, date range, and hours/day
- Live validation of request dates (start ≤ end) before submission
- Track request history and status (Pending / Approved)

### ✅ Resource Approval Workflow
- Review pending requests in one place
- **Smart availability suggestions** — eligible engineers are automatically labeled as *100% Free*, *Partially booked*, or *Overloaded* based on their current schedule
- "Before vs. after" capacity preview showing projected peak daily load before confirming an assignment
- Assignment is blocked automatically if it would push an engineer over the daily hour limit

### 📊 Capacity Visualization
- **Availability Heatmap** — 21-day outlook per engineer, color-coded from free (green) to overloaded (red)
- **Stacked Capacity Chart** — daily hours per engineer, broken down by project, with a threshold line at the daily limit
- **Interactive Gantt Timeline** — project assignments grouped by engineer
- Department-level filtering across all views

### 🛠️ Administration
- One-click reset of all application data back to its default demo configuration

## Tech Stack

| Layer | Technology |
|---|---|
| App framework | [Streamlit](https://streamlit.io/) |
| Data handling | [Pandas](https://pandas.pydata.org/) |
| Visualization | [Plotly](https://plotly.com/python/) |
| Testing | Python `unittest` |
| Project management | Jira Software (Agile/Scrum) |
| Version control | Git / GitHub |

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/MInesGomes/BPProjManag.git
cd BPProjManag

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate    # on Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

> [!NOTE]
> `requirements.txt` currently lists `streamlit` and `plotly`. Pandas is installed automatically as a Streamlit dependency, but if you run into an import error, install it explicitly with `pip install pandas`.

### Running the app

```bash
streamlit run ProjManagement.py
```

Streamlit will open the app in your browser at `http://localhost:8501`.

## Project Structure

```
BPProjManag/
├── ProjManagement.py            # Streamlit UI: pages, forms, charts
├── proj_management_logic.py     # Core business logic (capacity checks, allocations)
├── test_proj_management_logic.py# Unit tests for the business logic
├── requirements.txt              # Python dependencies
└── .gitignore
```

## Usage Guide

The sidebar lets you switch roles to simulate different logins — there's no authentication, this is a demo/prototype environment seeded with sample engineers, departments, and projects.

**As a Project Manager, you can:**
1. Select a project, required department, date range, and hours/day
2. Submit the request — it appears as "Pending" for a Department Manager to act on
3. Track the status of all your requests in the table below the form

**As a Department Manager, you can:**
1. Pick a pending request to review
2. Choose from the eligible engineers, each labeled with their current availability
3. Check the projected capacity impact before confirming
4. Confirm the assignment (blocked if it would overload the engineer)
5. Explore the Heatmap, Stacked Capacity, and Gantt tabs to review team-wide workload, optionally filtered by department

Use **Reset Entire Application** in the sidebar at any time to clear all requests/allocations and start over with the default sample data.

## Running Tests

```bash
python -m unittest
```

This runs the unit tests in `test_proj_management_logic.py` against the capacity-checking logic in `proj_management_logic.py`.

## Project Methodology

This project was developed using **Agile/Scrum**, chosen over Waterfall because resource-allocation requirements were expected to change frequently and benefit from iterative delivery and continuous feedback.

Work was tracked in Jira across 3 sprints and 5 epics (Resource Request Management, Resource Approval Workflow, Capacity Planning, Capacity Visualization, Administration):

| Sprint | Goal |
|---|---|
| **1 — Resource Request Workflow** | Enable Project Managers to submit requests and Department Managers to assign engineers |
| **2 — Capacity Management** | Provide workload analysis and prevent engineer overallocation |
| **3 — Capacity Analytics & Reporting** | Deliver heatmaps, capacity charts, Gantt timelines, and filtering |

Testing was managed with Xray Test Management alongside Python's `unittest`.
---

# 💡 Proposed Solution

ResSync provides a centralized platform for resource planning, allocation, and workload analysis.

The system allows:

### Project Managers
- Submit resource requests
- Monitor request status
- View assigned engineers

### Department Managers
- Review pending requests
- Assign engineers to projects
- Monitor engineer utilization
- Prevent resource overallocation
- Analyze team capacity using dashboards

The application automatically evaluates engineer workloads and prevents assignments that exceed capacity thresholds.

---

# ✨ Key Features

## Resource Request Management
- Submit resource requests
- View request history
- Track request status

## Resource Approval Workflow
- Review pending requests
- Assign engineers
- Update approval status automatically

## Capacity Planning
- Daily workload calculations
- Weekly capacity management
- Smart availability recommendations
- Overload prevention

## Capacity Visualization
- Availability Heatmap
- Stacked Capacity Chart
- Interactive Gantt Timeline
- Department-level filtering

## Administration
- Reset application data
- Restore default configuration

---

# 🏗️ Main Requirements

### Role Management
The system distinguishes between:
- Project Manager
- Department Manager

### Capacity Tracking
The system supports:
- Weekly capacities of 32 or 40 hours
- Daily workload limit of 12 hours
- Engineer utilization monitoring

### Workflow Management
The system supports:
- Creation of resource requests
- Capacity evaluation
- Engineer assignment
- Request approval

### Reporting
The application provides:
- Heatmaps
- Capacity charts
- Gantt timelines
- Utilization dashboards

---

# 🧩 Project Methodology

## Waterfall

Waterfall follows a structured and sequential development process where requirements, design, implementation, testing, and deployment are completed in separate phases. Although this approach provides strong documentation and planning, it is less suitable for projects with frequently changing requirements.

## Agile / Scrum

Agile Scrum delivers software incrementally through short development cycles called sprints. It supports continuous feedback, flexibility, stakeholder involvement, and iterative improvement.

### Why Agile Was Chosen

Agile Scrum was selected because resource allocation requirements are dynamic and can change frequently. The methodology enables:

- Rapid delivery of working functionality
- Continuous stakeholder feedback
- Incremental enhancement of features
- Better adaptability to changing business needs

---

# 🏃 Sprint Plan

## Sprint 1 – Resource Request Workflow

Goal: Enable Project Managers to submit requests and Department Managers to assign engineers.

Stories:
- Submit Resource Request
- View Submitted Requests
- View Pending Requests
- Assign Engineer

---

## Sprint 2 – Capacity Management

Goal: Provide workload analysis and prevent engineer overallocation.

Stories:
- Prevent Engineer Overload
- Display Utilization Analysis
- Smart Availability Recommendation

---

## Sprint 3 – Capacity Analytics & Reporting

Goal: Deliver reporting and visualization functionality.

Stories:
- Heatmap Visualization
- Stacked Capacity Chart
- Gantt Timeline
- Filter By Department
- Reset Application Data

---

# 📋 Jira Project Structure

The project was managed using Jira Software and organized into five Epics:

### Resource Request Management
- Submit Resource Request
- View Submitted Requests

### Resource Approval Workflow
- View Pending Requests
- Assign Engineer
- Prevent Engineer Overload

### Capacity Planning
- Display Utilization Analysis
- Smart Availability Recommendation

### Capacity Visualization
- Heatmap Visualization
- Stacked Capacity Chart
- Gantt Timeline
- Filter By Department

### Administration
- Reset Application Data

The project contains:
- 5 Epics
- 12 User Stories
- 3 Sprints
- Story Points
- Sprint Backlogs


