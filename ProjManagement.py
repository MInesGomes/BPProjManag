import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Setup & Config ---
st.set_page_config(page_title="Resources Sync - Resource Allocation", layout="wide")

st.title("🗓️ Resources Sync: Resource Workflow Portal")
st.markdown("A two-step workflow featuring **Smart Capacity Approvals**, **Availability Heatmaps**, and **Stacked Workload Analysis**.")

# --- Session State Initialization ---
def initialize_session_state():
    if 'engineers_list' not in st.session_state:
        st.session_state.engineers_list = [f"Engineer {i}" for i in range(1, 16)]
        st.session_state.departments_list = ["Backend", "Frontend", "DevOps", "QA", "Data Science"]
        st.session_state.capacities = {f"Engineer {i}": (32 if i % 3 == 0 else 40) for i in range(1, 16)}
        
        st.session_state.eng_dept_map = {}
        for i, eng in enumerate(st.session_state.engineers_list):
            dept = st.session_state.departments_list[i % len(st.session_state.departments_list)]
            st.session_state.eng_dept_map[eng] = dept

    if 'projects_df' not in st.session_state:
        base_date = datetime.today() - timedelta(days=datetime.today().weekday())
        projects_data = []
        project_names = ["Project Alpha", "Project Beta", "Project Gamma", "Project Delta", "Project Epsilon"]
        for idx, p_name in enumerate(project_names):
            start_dt = base_date + timedelta(days=idx*7)
            end_dt = start_dt + timedelta(days=60)
            projects_data.append({"Project": p_name, "Proj Start": start_dt.date(), "Proj End": end_dt.date()})
        st.session_state.projects_df = pd.DataFrame(projects_data)

    if 'requests' not in st.session_state:
        base_date = datetime.today() - timedelta(days=datetime.today().weekday())
        st.session_state.requests = pd.DataFrame([{
            "Req ID": 1001,
            "Project": "Project Alpha",
            "Required Dept": "QA",
            "Start Date": base_date.date(),
            "End Date": (base_date + timedelta(days=14)).date(),
            "Hours/Day": 4,
            "Status": "Pending",
            "Assigned Engineer": "None"
        }])
        st.session_state.next_req_id = 1002

    if 'allocations' not in st.session_state:
        st.session_state.allocations = pd.DataFrame(columns=[
            "Engineer", "Department", "Project", "Start Date", "End Date", "Hours/Day", "Linked Req ID"
        ])

# --- Page Setup & Config ---
def get_daily_load(target_eng, start_date, end_date):
    """Returns a dict of {date: total_hours} for an engineer in a given date range (Business days only)."""
    df = st.session_state.allocations
    eng_allocs = df[df["Engineer"] == target_eng]
    dates = pd.date_range(start=start_date, end=end_date, freq='B')
    daily_hours = {d.date(): 0 for d in dates}
    
    for _, row in eng_allocs.iterrows():
        overlap_dates = pd.date_range(start=max(start_date, row["Start Date"]), 
                                      end=min(end_date, row["End Date"]), freq='B')
        for ed in overlap_dates:
            if ed.date() in daily_hours:
                daily_hours[ed.date()] += row["Hours/Day"]
    return daily_hours


# ==========================================
#         Session State Initialization
# ==========================================
initialize_session_state()

# --- Sidebar: Role Switcher & System Reset ---
st.sidebar.header("👤 User Role")
user_role = st.sidebar.radio("Login as:", ["Project Manager", "Department Manager"])

st.sidebar.markdown("---")
if st.sidebar.button("⚠️ Reset Entire Application"):
    st.session_state.clear()
    st.rerun()

# ==========================================
#         PROJECT MANAGER VIEW
# ==========================================
if user_role == "Project Manager":
    st.markdown("## 📊 Project Manager Dashboard")
    col_req, col_proj = st.columns([1, 1])
    
    with col_req:
        st.subheader("📝 Request Project Resources")
        
        # 🟢 Removed st.form wrapper, using a simple container for style
        with st.container(border=True):
            req_proj = st.selectbox("Select Project", st.session_state.projects_df["Project"])
            req_dept = st.selectbox("Required Role (Department)", st.session_state.departments_list)
            req_start = st.date_input("Need Start Date", datetime.today())
            req_end = st.date_input("Need End Date", datetime.today() + timedelta(days=14))
            req_hrs = st.slider("Hours per Day Required", min_value=1, max_value=8, value=4)
            
            # ⚡ LIVE CHECK: triggers when the user changes a date!
            dates_are_invalid = req_start > req_end
            if dates_are_invalid:
                st.error("⚠️ Rule Violation: Start Date must be before or equal to End Date.")
                
            # Disable the submit button completely if dates are invalid
            submitted = st.button("Submit Request to Department Manager", disabled=dates_are_invalid)
            
            if submitted:
                new_req = pd.DataFrame([{
                    "Req ID": st.session_state.next_req_id, "Project": req_proj,
                    "Required Dept": req_dept, "Start Date": req_start, "End Date": req_end,
                    "Hours/Day": req_hrs, "Status": "Pending", "Assigned Engineer": "None"
                }])
                st.session_state.requests = pd.concat([st.session_state.requests, new_req], ignore_index=True)
                st.session_state.next_req_id += 1
                st.success("Request submitted successfully!")
                st.rerun()

    with col_proj:
        st.subheader("📁 Project Directory")
        st.dataframe(st.session_state.projects_df, width='stretch', hide_index=True)
        
    st.markdown("---")
    st.subheader("📡 Status of My Requests")
    st.dataframe(st.session_state.requests, width='stretch', hide_index=True)

# ==========================================
#         DEPARTMENT MANAGER VIEW
# ==========================================
elif user_role == "Department Manager":
    st.markdown("## 🛠️ Department Manager Dashboard")
    
    # --- 1. Pending Requests & SMART Approvals ---
    st.subheader("🔔 Action Required: Pending Requests")
    pending_reqs = st.session_state.requests[st.session_state.requests["Status"] == "Pending"]
    
    if not pending_reqs.empty:
        # We don't use st.form here so the UI can be fully reactive/dynamic
        approval_container = st.container(border=True)
        with approval_container:
            selected_req_id = st.selectbox("Select a Request to process:", pending_reqs["Req ID"])
            req_details = pending_reqs[pending_reqs["Req ID"] == selected_req_id].iloc[0]
            
            r_dept = req_details["Required Dept"]
            r_hrs = req_details["Hours/Day"]
            r_start = req_details["Start Date"]
            r_end = req_details["End Date"]
            
            st.info(f"**Requested:** {req_details['Project']} needs a **{r_dept}** for **{r_hrs}h/day** from **{r_start}** to **{r_end}**.")
            
            # --- FEATURE 1: Smart Availability Dropdown ---
            eligible_engineers = [eng for eng, dept in st.session_state.eng_dept_map.items() if dept == r_dept]
            
            smart_options = {}
            for eng in eligible_engineers:
                daily_load = get_daily_load(eng, r_start, r_end)
                max_daily = max(daily_load.values()) if daily_load else 0
                weekly_cap = st.session_state.capacities[eng]
                
                # Check 5-day rolling sum for weekly cap approximate
                is_daily_ok = (max_daily + r_hrs) <= 12
                # Rough check: if peak day + requested > daily equivalent of weekly cap
                is_weekly_ok = ((max_daily + r_hrs) * 5) <= (weekly_cap + 10) # Added buffer for flexibility
                
                if not is_daily_ok or not is_weekly_ok:
                    status = "⛔ Overloaded"
                elif max_daily == 0:
                    status = "✅ 100% Free"
                else:
                    status = f"⚠️ Partial ({max_daily}h booked)"
                    
                smart_options[eng] = f"{eng} — {status}"

            selected_eng_key = st.selectbox(
                "Select Engineer to Evaluate:", 
                options=eligible_engineers,
                format_func=lambda x: smart_options[x]
            )
            
            # --- FEATURE 2: "Before & After" Progress Bars ---
            if selected_eng_key:
                st.markdown(f"#### Capacity Analysis: {selected_eng_key}")
                daily_load = get_daily_load(selected_eng_key, r_start, r_end)
                current_peak = max(daily_load.values()) if daily_load else 0
                projected_peak = current_peak + r_hrs
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.caption(f"Current Peak Daily Load: {current_peak}h / 12h")
                    st.progress(min(current_peak / 12.0, 1.0))
                with col_b2:
                    if projected_peak <= 12:
                        st.caption(f"Projected Peak Daily Load: {projected_peak}h / 12h ✅ Safe")
                        st.progress(min(projected_peak / 12.0, 1.0))
                    else:
                        st.error(f"Projected Peak Daily Load: {projected_peak}h / 12h ⛔ Exceeds 12h Limit!")
                
                # Submit logic
                can_approve = projected_peak <= 12
                if st.button("Confirm & Assign Resource", type="primary", disabled=not can_approve):
                    new_alloc = pd.DataFrame([{
                        "Engineer": selected_eng_key, "Department": r_dept, "Project": req_details["Project"],
                        "Start Date": r_start, "End Date": r_end, "Hours/Day": r_hrs, "Linked Req ID": selected_req_id
                    }])
                    st.session_state.allocations = pd.concat([st.session_state.allocations, new_alloc], ignore_index=True)
                    
                    req_idx = st.session_state.requests.index[st.session_state.requests["Req ID"] == selected_req_id].tolist()[0]
                    st.session_state.requests.at[req_idx, "Status"] = "Approved"
                    st.session_state.requests.at[req_idx, "Assigned Engineer"] = selected_eng_key
                    
                    st.success(f"Successfully assigned {selected_eng_key}!")
                    st.rerun()
    else:
        st.success("🎉 All requests have been processed!")

    # --- 2. Advanced Visualizations (Heatmap & Stacked Bars) ---
    st.markdown("---")
    st.subheader("📈 Department Capacity Dashboard")
    
    all_departments = ["All Departments"] + st.session_state.departments_list
    selected_dept = st.selectbox("Filter Visualizations by Department:", all_departments)
    
    # Filter engine
    if selected_dept == "All Departments":
        viz_allocs = st.session_state.allocations
        target_engineers = st.session_state.engineers_list
    else:
        viz_allocs = st.session_state.allocations[st.session_state.allocations["Department"] == selected_dept]
        target_engineers = [eng for eng, dept in st.session_state.eng_dept_map.items() if dept == selected_dept]

    # Generate Date Range for Heatmap/Stacked Bar (Next 14 Days)
    today_date = datetime.today().date()
    future_date = today_date + timedelta(days=21)
    business_days = pd.date_range(start=today_date, end=future_date, freq='B').date
    
    # Pre-calculate matrix data
    matrix_data = []
    for eng in target_engineers:
        eng_daily = get_daily_load(eng, today_date, future_date)
        for d in business_days:
            matrix_data.append({"Engineer": eng, "Date": d, "Assigned Hours": eng_daily.get(d, 0)})
    
    matrix_df = pd.DataFrame(matrix_data)

    # Use tabs for clean UI
    tab1, tab2, tab3, tab4 = st.tabs(["🔥 Availability Heatmap", "📊 Stacked Capacity Bar", "📅 Gantt Timeline", "📋 Raw Data"])

    with tab1:
        st.markdown("**14-Day Outlook Heatmap** (Green = Free, Red = Overloaded)")
        if not matrix_df.empty:
            pivot_df = matrix_df.pivot(index="Engineer", columns="Date", values="Assigned Hours")
            # Convert columns to string for cleaner plotly rendering
            pivot_df.columns = [col.strftime('%b %d') for col in pivot_df.columns]
            
            fig_heat = px.imshow(
                pivot_df,
                labels=dict(x="Date", y="Engineer", color="Assigned Hours"),
                x=pivot_df.columns,
                y=pivot_df.index,
                color_continuous_scale="RdYlGn_r", # Green to Red reversed
                zmin=0, zmax=12,
                aspect="auto"
            )
            fig_heat.update_xaxes(side="top")
            fig_heat.update_layout(height=400)
            st.plotly_chart(fig_heat, width='stretch')

    with tab2:
        st.markdown("**Daily Project Load per Engineer** (Visualizing specific project stack)")
        if not viz_allocs.empty:
            # We need to expand allocations into daily records for the stacked bar
            bar_data = []
            for _, row in viz_allocs.iterrows():
                overlap_dates = pd.date_range(start=max(today_date, row["Start Date"]), 
                                              end=min(future_date, row["End Date"]), freq='B')
                for d in overlap_dates:
                    bar_data.append({
                        "Engineer": row["Engineer"], "Date": d.date(), 
                        "Project": row["Project"], "Hours": row["Hours/Day"]
                    })
            bar_df = pd.DataFrame(bar_data)
            
            if not bar_df.empty:
                # Group by to stack appropriately
                fig_bar = px.bar(
                    bar_df, x="Date", y="Hours", color="Project", facet_row="Engineer",
                    title="Stacked Daily Hours", category_orders={"Engineer": target_engineers}
                )
                
                # Add a red threshold line at 12 hours for all subplots
                fig_bar.add_hline(y=12, line_dash="dash", line_color="red", annotation_text="Max 12h")
                
                # Clean up facet layout
                fig_bar.update_layout(height=150 * len(target_engineers), showlegend=True)
                fig_bar.update_yaxes(matches=None, title="Hours")
                st.plotly_chart(fig_bar, width='stretch')
            else:
                st.info("No projects scheduled in the next 14 days.")
        else:
            st.info("No allocations exist for the selected filter.")

    with tab3:
        st.markdown("**Classic Project Gantt Chart** (Grouped by Engineer)")
        if not viz_allocs.empty:
            # 1. Create a copy to avoid SettingWithCopyWarning
            viz_allocs_gantt = viz_allocs.copy()
            
            # 2. Create a unique Y-axis label
            viz_allocs_gantt["Timeline_Y"] = viz_allocs_gantt["Engineer"] + " ➔ " + viz_allocs_gantt["Project"]
            
            # 3. Sort the dataframe explicitly by Engineer, then by Start Date
            viz_allocs_gantt = viz_allocs_gantt.sort_values(by=["Engineer", "Start Date"])
            
            # 4. Extract the exact ordered list of Y-axis labels
            # Because the dataframe is sorted by Engineer, unique() will keep all of one engineer's rows together
            ordered_y_axis = viz_allocs_gantt["Timeline"].unique().tolist()

            fig_gantt = px.timeline(
                viz_allocs_gantt, 
                x_start="Start Date", 
                x_end="End Date",
                y="Timeline", 
                color="Project", 
                hover_data=["Hours/Day", "Engineer"],
                color_discrete_sequence=px.colors.qualitative.Safe
            )
            
            # 5. Force Plotly to respect our custom grouped array
            fig_gantt.update_yaxes(
                autorange="reversed",
                categoryorder="array",
                categoryarray=ordered_y_axis,
                tickmode="linear",
                dtick=4
            )
            st.plotly_chart(fig_gantt, use_container_width=True)
            
            # Dynamic height based on the number of unique rows, not total dataframe length
            dynamic_height = max(400, len(ordered_y_axis) * 40)
            fig_gantt.update_layout(height=dynamic_height)
            
            st.plotly_chart(fig_gantt, width='stretch')
        else:
            st.info("No approved allocations yet for timeline.")    

    with tab4:
        st.markdown("**Approved Allocations Matrix**")
        st.dataframe(viz_allocs, width='stretch', hide_index=True)
