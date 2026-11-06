import streamlit as st
from streamlit_option_menu import option_menu
import altair as alt
import pandas as pd
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="EduRisk Analytics - Lab 05",
    page_icon="🎓",
    layout="wide"
)

# Student Dataset
def load_student_data():
    try:
        data = pd.read_csv("students.csv")
        return data
    except FileNotFoundError:
        st.error(
            "students.csv was not found. Please place it in the same folder as app.py."
        )
        st.stop()

student_df = load_student_data()

# Risk level function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(
        row["Score"],
        row["Attendance"]
    ),
    axis=1
)

# Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

# Initialize Session State
if "risk_history" not in st.session_state:
    st.session_state["risk_history"] = []

# Sidebar Navigation
with st.sidebar:
    selected_page = option_menu(
        menu_title="Menu",  # Header of the sidebar
        options=["Home", "Dashboard", "Student Data", "Risk Checker", "About"],
        # Add cool icons for each page (optional but looks great!)
        icons=["house", "bar-chart-line", "table", "shield-check", "info-circle"],
        default_index=0, # Starts on the first page
    )

# Home page
if selected_page == "Home":
    st.title("🎓 EduRisk Analytics")
    st.subheader("Interactive Dashboard with Visualization and Filters")
    st.write("Welcome to Lab 05.")
    st.write(
        "In this lab, the app improves the Dashboard page using "
        "grouped summaries, interactive filters, Streamlit charts, and Plotly charts."
    )
    st.success("Lab 05 app is running successfully!")

# Dashboard page
elif selected_page == "Dashboard":
    st.title("Interactive Student Performance Dashboard")

    st.write(
        "Use filters to explore student performance by course, risk level, "
        "and attendance. The dashboard updates based on your selections."
    )

    st.subheader("Dashboard Filters")

    filter_col1, filter_col2, filter_col3 = st.columns(3)

    with filter_col1:
        course_options = ["All"] + sorted(student_df["Course"].unique())
        selected_course = st.selectbox(
            "Filter by Course",
            course_options
        )

    with filter_col2:
        risk_options = ["All"] + sorted(student_df["Risk Level"].unique())
        selected_risk = st.selectbox(
            "Filter by Risk Level",
            risk_options
        )

    with filter_col3:
        minimum_attendance = st.slider(
            "Minimum Attendance",
            0,
            100,
            0
        )

    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[
            filtered_df["Course"] == selected_course
        ]

    if selected_risk != "All":
        filtered_df = filtered_df[
            filtered_df["Risk Level"] == selected_risk
        ]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= minimum_attendance
    ]

    if filtered_df.empty:
        st.warning("No students match the selected filters. Please adjust the filters.")

    st.subheader("Filtered Dashboard Metrics")

    filtered_total_students = len(filtered_df)

    if filtered_total_students > 0:
        filtered_average_score = filtered_df["Score"].mean()
        filtered_average_attendance = filtered_df["Attendance"].mean()
        filtered_high_risk_students = filtered_df[
            filtered_df["Risk Level"] == "High Risk"
        ].shape[0]
    else:
        filtered_average_score = 0
        filtered_average_attendance = 0
        filtered_high_risk_students = 0

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Students", filtered_total_students)

    with metric_col2:
        st.metric("Average Score", round(filtered_average_score, 2))

    with metric_col3:
        st.metric(
            "Average Attendance",
            f"{round(filtered_average_attendance, 2)}%"
        )

    with metric_col4:
        st.metric("High Risk", filtered_high_risk_students)

    st.subheader("Course Summary")

    if filtered_total_students > 0:
        course_summary = filtered_df.groupby("Course").agg(
            Students=("Student Name", "count"),
            Average_Score=("Score", "mean"),
            Average_Attendance=("Attendance", "mean"),
            Average_Study_Hours=("Study Hours", "mean")
        ).reset_index()

        st.dataframe(course_summary)
    else:
        st.info("No course summary available for the selected filters.")

    st.subheader("Risk Level Summary")

    if filtered_total_students > 0:
        risk_summary = filtered_df["Risk Level"].value_counts().reset_index()
        risk_summary.columns = ["Risk Level", "Students"]

        st.dataframe(risk_summary)
    else:
        st.info("No risk summary available for the selected filters.")

    st.subheader("Streamlit Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if filtered_total_students > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.info("No score chart available.")

    with chart_col2:
        st.write("Students by Course")

        if filtered_total_students > 0:
            course_count = filtered_df["Course"].value_counts()
            st.bar_chart(course_count)
        else:
            st.info("No course count chart available.")

    st.subheader("Interactive Plotly Charts")

    plotly_col1, plotly_col2 = st.columns(2)

    with plotly_col1:
        st.write("Risk Level Distribution")

        if filtered_total_students > 0:
            risk_summary_chart = filtered_df["Risk Level"].value_counts().reset_index()
            risk_summary_chart.columns = ["Risk Level", "Students"]

            fig_risk = px.bar(
                risk_summary_chart,
                x="Risk Level",
                y="Students",
                color="Risk Level",
                title="Risk Level Distribution",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_risk, use_container_width=True)
        else:
            st.info("No risk distribution chart available.")

    with plotly_col2:
        st.write("Student Scores by Risk Level")

        if filtered_total_students > 0:
            fig_score = px.bar(
                filtered_df,
                x="Student Name",
                y="Score",
                color="Risk Level",
                title="Student Scores by Risk Level",
                color_discrete_map={
                    "Low Risk": "#16A34A",
                    "Medium Risk": "#F59E0B",
                    "High Risk": "#DC2626"
                }
            )

            st.plotly_chart(fig_score, use_container_width=True)
        else:
            st.info("No score chart available.")

    st.subheader("Filtered Student Records")

    if filtered_total_students > 0:
        st.dataframe(filtered_df)
    else:
        st.info("No student records to display.")

    st.warning(
        "Ethics Reminder: Visualizations should support students and guide "
        "academic support decisions, not label or punish students."
    )

# Student data page
elif selected_page == "Student Data":
    st.title("Student Data")

    st.write(
        "This page displays and inspects the dataset loaded from students.csv."
    )

    st.subheader("Data Inspection")

    st.write("Rows and Columns:", student_df.shape)

    st.write("Column Names:")
    st.write(student_df.columns.tolist())

    st.write("First 5 Rows:")
    st.dataframe(student_df.head())

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

# Risk checker page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    st.write(
        "Enter student information to check risk level. "
        "The result is based on score and attendance."
    )

    st.info(
        "This tool is for academic support. Risk results should help students, "
        "not label or punish them."
    )
    
    st.divider() # ADDED DIVIDER

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)

        submitted = st.form_submit_button("Check Risk")

    if submitted:
        if input_name.strip() == "":
            st.warning("Please enter the student name.")
        else:
            risk_result = get_risk_level(
                input_score,
                input_attendance
            )

            result = {
                "Student Name": input_name.strip(),
                "Score": input_score,
                "Attendance": input_attendance,
                "Risk Level": risk_result
            }

            st.session_state["risk_history"].append(result)

            if risk_result == "Low Risk":
                st.success("Risk Level: Low Risk")
                st.write("Student appears on track.")
            elif risk_result == "Medium Risk":
                st.warning("Risk Level: Medium Risk")
                st.write("Monitor progress and provide guidance.")
            else:
                st.error("Risk Level: High Risk")
                st.write("Student may need additional support.")

            st.write("Student Name:", input_name.strip())
            st.write("Score:", input_score)
            st.write("Attendance:", input_attendance)

    st.subheader("Recent Risk Checks")

    if len(st.session_state["risk_history"]) > 0:
        history_df = pd.DataFrame(
            st.session_state["risk_history"]
        )

        st.dataframe(history_df)

        if st.button("Clear History"):
            st.session_state["risk_history"] = []
            st.success("Risk check history cleared.")
    else:
        st.info("No risk checks yet.")

    st.warning(
        "Ethics Reminder: Risk results should be used as guidance for support, "
        "not as final judgment about a student."
    )

# About page
else:
    st.title("About")

    st.write("This app is part of Lab 05.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Visualization and Interactivity")

    st.info(
        "This version improves the Dashboard page using grouped summaries, "
        "interactive filters, Streamlit charts, and Plotly charts."
    )

    st.warning(
        "Ethics Reminder: Student performance visualizations should be used "
        "responsibly to support learning and student success."
    )