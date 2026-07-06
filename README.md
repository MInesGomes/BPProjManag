#### 1. Business Problem & Proposed Software Solution
 
* **The Business Problem:** Companies often struggle to allocate shared engineering resources across multiple projects and departments. Using spreadsheets leads to scheduling conflicts, lack of visibility into daily workload limits (e.g., maximum 12 hours/day), and inefficient tracking of unallocated staff.
* **The Proposed Software Solution:** "ResSync" – a centralized, web-based Resource Workflow Portal. It allows Project Managers to submit resource requests and enables Department Managers to visually review capacity, approve requests, and assign engineers using smart availability tracking and Gantt chart visualizations.
 
#### 2. Main Requirements
 
* **Role Management:** The system must differentiate between Project Managers (requestors) and Department Managers (approvers).
* **Capacity Tracking:** The system must track weekly capacities (32h or 40h) and enforce a daily maximum limit of 12 hours per engineer.
* **Visualizations:** The dashboard must include a timeline (Gantt chart) for scheduling, a workload heatmap, and a capacity progress bar.
* **Workflow:** The system must allow pending requests to be created, evaluated against available capacity, and formally approved.
 
#### 3. Methodology: Waterfall vs. Agile/Scrum
 
* **Waterfall:** A linear, sequential approach to software design where progress flows downwards through phases like Conception, Initiation, Analysis, Design, Construction, Testing, and Deployment (PMI, 2021). It requires strict, unchanging requirements from the start.
* **Agile/Scrum:** An iterative and incremental framework. Work is divided into short cycles called "Sprints" (usually 1-4 weeks). It emphasizes continuous feedback, adaptability, and cross-functional team collaboration (Schwaber & Sutherland, 2020 - The Scrum Guide).
* **Appropriate Methodology:** For ResSync, **Agile/Scrum** is the most appropriate methodology. Resource allocation needs are highly dynamic. Agile allows the team to build a minimum viable prototype (like our Streamlit app), gather feedback from Project Managers on the UI/UX, and iteratively add features like the "Availability Heatmap" in subsequent sprints.
