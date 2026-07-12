
# 🚀 Resources Sync: Resource Workflow Portal (ResSync)

ResSync is a Streamlit-based resource allocation and capacity planning platform designed to help organizations manage engineers across multiple projects while preventing resource overallocation and improving resource visibility.

---

# 📖 Overview

The ResSync was developed to address the challenges of managing shared engineering resources across multiple concurrent projects. The application enables Project Managers to submit resource requests and Department Managers to evaluate capacity, approve requests, and assign engineers using real-time workload analysis and visualization tools.

---

# 🎯 Business Problem

Organizations frequently manage multiple projects while sharing a limited pool of engineers. Resource allocation is often handled through spreadsheets and manual communication, leading to:

- Resource overallocation
- Scheduling conflicts
- Limited visibility into engineer workloads
- Delayed project delivery
- Inefficient staffing decisions
- Difficulty tracking resource availability

As project complexity increases, manual resource planning becomes difficult to maintain and prone to errors.

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

---

# 🛠️ Technology Stack

### Development
- Python
- Streamlit

### Data Processing
- Pandas

### Visualization
- Plotly

### Project Management
- Jira Software

### Testing
- Xray Test Management
- Python unittest

### Version Control
- GitHub

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/MInesGomes/BPProjManag.git
cd BPProjManag
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Run Application

```bash
streamlit run app.py
```

## 4. Execute Unit Tests

```bash
python -m unittest
```
