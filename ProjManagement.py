import streamlit as st 
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- Page Setup & Config ---
st.set_page_config(page_title="ResSync - Resource Allocation", layout="wide")
st.title("🗓️ ResSync: Shared Engineer Allocation Portal")
st.markdown("Easily schedule and track **15 Engineers** across **5 Departments** and **5 Active Projects**.")

# --- Mock Data Construction ---
if 'allocations' not in st.session_state:
    # Set up our initial parameters
    engineers = [f"Engineer {i}" for i in range(1, 16)]
    departments = ["Backend", "Frontend", "DevOps", "QA", "Data Science"]
    projects = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Epsilon"]
    
    # Establish a default timeline baseline starting Monday
    base_date = datetime.today() - timedelta(days=datetime.today().weekday())
    
    # Generate balanced baseline data records
    initial_data = []
    for i, eng in enumerate(engineers):
        dept = departments[i % len(departments)]
        proj = projects[i % len(projects)]
        initial_data.append({
            "Engineer": eng,
            "Department": dept,
            "Project": proj,
            "Start Date": (base_date).date(),
            "End Date": (base_date + timedelta(days=5)).date()
        })
    st.session_state.allocations = pd.DataFrame(initial_data)
    st.session_state.projects = projects

# --- Sidebar Management Controls ---
st.sidebar.header("🔧 Update Weekly Allocation")
with st.sidebar.form("allocation_form", clear_on_submit=False):
    target_eng = st.selectbox("Select Engineer", st.session_state.allocations["Engineer"].unique())
    new_proj = st.selectbox("Assign to Project", st.session_state.projects)
    
    # Simple calendar week adjustments
    start_input = st.date_input("Allocation Start", datetime.today())
    end_input = st.date_input("Allocation End", datetime.today() + timedelta(days=5))
    
    submit = st.form_submit_button("Update Schedule")
    
    if submit:
        if start_input > end_input:
            st.sidebar.error("Error: Start Date must occur before End Date.")
        else:
            # Overwrite active engineering parameters
            idx = st.session_state.allocations[st.session_state.allocations["Engineer"] == target_eng].index[0]
            st.session_state.allocations.at[idx, "Project"] = new_proj
            st.session_state.allocations.at[idx, "Start Date"] = start_input
            st.session_state.allocations.at[idx, "End Date"] = end_input
            st.sidebar.success(f"Successfully reassigned {target_eng}!")

# --- Main Dashboard Visualization Layout ---
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Visual Gantt Timeline View")
    
    # Generate the timeline graph using Plotly
    fig = px.timeline(
        st.session_state.allocations,
        x_start="Start Date",
        x_end="End Date",
        y="Engineer",
        color="Project",
        hover_data=["Department"],
        title="Weekly Schedule Overview",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    
    # Match timeline axis rendering expectations 
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis_title="Timeline Calendar",
        yaxis_title="Shared Engineers Pool",
        height=550,
        legend_title="Active Projects"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Data Summary Matrix")
    # Display project engineering counts
    proj_counts = st.session_state.allocations["Project"].value_counts()
    st.dataframe(proj_counts, column_config={"count": "Engineers Assigned"})
    
    st.markdown("---")
    st.markdown("""
    **Dashboard KPIs:**
    * Total Engineers: `15`
    * Active Projects: `5`
    * Total Managed Departments: `5`
    """)

# --- Tabular Overview Grid ---
st.subheader("Detailed Allocation Matrix Table")
st.dataframe(st.session_state.allocations, use_container_width=True)
