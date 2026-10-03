import streamlit as st
from streamlit_option_menu import option_menu
import altair as alt
import pandas as pd

# Configure page
st.set_page_config(
    page_title="EduRisk Analytics - Lab 02",
    page_icon="🎓",
    layout="wide"
)

# Student Dataset
student_df = pd.DataFrame({
    "Student Name": ["Dara", "Sophea", "Vuthy", "Malis", "Rithy", "Sreyneang", "Chan", "Bopha"],
    "Course": ["Python", "Statistics", "Python", "Database", "Web App", "Database", "Python", "Statistics"],
    "Score": [85, 68, 45, 92, 58, 91, 72, 62],
    "Attendance": [90, 75, 50, 95, 60, 94, 80, 88],
    "Study Hours": [12, 8, 3, 15, 5, 14, 9, 7]
})

# Risk level function
def get_risk_level(score, attendance):
    if score < 60 or attendance < 60:
        return "High Risk"
    elif score < 75 or attendance < 75:
        return "Medium Risk"
    else:
        return "Low Risk"

# Risk Level Column
student_df["Risk Level"] = student_df.apply(
    lambda row: get_risk_level(row["Score"], row["Attendance"]),
    axis=1
)

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
    st.subheader("Interactive Student Risk Monitoring Dashboard")
    st.write("Welcome to Lab 02.")
    st.write("In this lab, you will use Streamlit widgets to explore student performance data.")
    st.success("Lab 02 app is running successfully!")

# Dashboard page
elif selected_page == "Dashboard":
    st.title("Interactive Dashboard")

    st.write("Use the filters below to explore student performance.")

    # Course filter
    selected_course = st.selectbox(
        "Select Course",
        ["All"] + list(student_df["Course"].unique())
    )

    # Risk Level filter
    selected_risk = st.selectbox(
        "Select Risk Level",
        ["All", "Low Risk", "Medium Risk", "High Risk"]
    )

    # Side-by-side boxed sliders
    slider_col1, slider_col2 = st.columns(2)

    # Minimum Attendance
    with slider_col1:
        with st.container(border=True):
            min_attendance = st.slider("Minimum Attendance", 0, 100, 0)

    # Minimum Score
    with slider_col2:
        with st.container(border=True):
            min_score = st.slider("Minimum Score", 0, 100, 0)

    # Filtering logic
    filtered_df = student_df.copy()

    if selected_course != "All":
        filtered_df = filtered_df[filtered_df["Course"] == selected_course]

    if selected_risk != "All":
        filtered_df = filtered_df[filtered_df["Risk Level"] == selected_risk]

    filtered_df = filtered_df[
        filtered_df["Attendance"] >= min_attendance
    ]

    filtered_df = filtered_df[
        filtered_df["Score"] >= min_score
    ]

    # Dashboard Metrics
    total_students = len(filtered_df)

    if len(filtered_df) > 0:
        average_score = filtered_df["Score"].mean()
        average_attendance = filtered_df["Attendance"].mean()
    else:
        average_score = 0
        average_attendance = 0

    high_risk_students = filtered_df[
        filtered_df["Risk Level"] == "High Risk"
    ].shape[0]

    st.subheader("Dashboard Metrics")

    # Create 4 columns for the metrics
    col1, col2, col3, col4 = st.columns(4)

    # Wrap each metric inside a bordered container
    with col1:
        with st.container(border=True):
            st.metric("Students", total_students)

    with col2:
        with st.container(border=True):
            st.metric("Average Score", round(average_score, 2))

    with col3:
        with st.container(border=True):
            st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        with st.container(border=True):
            st.metric("High Risk", high_risk_students)

    # Show/Hide dataset checkbox
    show_data = st.checkbox("Show Filtered Dataset", True)

    if show_data:
        st.subheader("Filtered Student Dataset")
        st.dataframe(filtered_df)

        # Download button
        csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered Data",
            data=csv,
            file_name="filtered_student_data.csv",
            mime="text/csv"
        )
    else:
        st.info("Filtered dataset is hidden.")


    # Student score chart
    st.subheader("Charts")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.write("Student Scores")

        if len(filtered_df) > 0:
            score_chart = filtered_df.set_index("Student Name")["Score"]
            st.bar_chart(score_chart)
        else:
            st.warning("No data available for score chart.")

    # Risk level count chart
    with chart_col2:
        st.write("Risk Level Count")

        if len(filtered_df) > 0:
            # Prepare data for Altair
            risk_count_df = filtered_df["Risk Level"].value_counts().reset_index()
            risk_count_df.columns = ["Risk Level", "Count"]

            # Create an Altair chart with custom colors
            risk_chart = alt.Chart(risk_count_df).mark_bar().encode(
                x=alt.X("Risk Level", sort=None),
                y="Count",
                color=alt.Color(
                    "Risk Level",
                    scale=alt.Scale(
                        domain=["Low Risk", "Medium Risk", "High Risk"],
                        range=["#28a745", "#ffc107", "#dc3545"] # Green, Yellow, Red
                    ),
                    legend=None # Hide legend since x-axis has the labels
                )
            )
            # Display the chart
            st.altair_chart(risk_chart, use_container_width=True)
        else:
            st.warning("No data available for risk chart.")

# Student data page
elif selected_page == "Student Data":
    st.title("Student Data")

    total_students = len(student_df)
    average_score = student_df["Score"].mean()
    average_attendance = student_df["Attendance"].mean()
    high_risk_students = student_df[
        student_df["Risk Level"] == "High Risk"
    ].shape[0]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        with st.container(border=True):
            st.metric("Total Students", total_students)

    with col2:
        with st.container(border=True):
            st.metric("Average Score", round(average_score, 2))

    with col3:
        with st.container(border=True):
            st.metric("Average Attendance", f"{round(average_attendance, 2)}%")

    with col4:
        with st.container(border=True):
            st.metric("High Risk Students", high_risk_students)

    st.subheader("Full Student Dataset")
    st.dataframe(student_df)

# Risk cheker page
elif selected_page == "Risk Checker":
    st.title("Single Student Risk Checker")

    with st.form("risk_checker_form"):
        input_name = st.text_input("Student Name")
        input_score = st.number_input("Score", 0, 100, 50)
        input_attendance = st.number_input("Attendance", 0, 100, 50)
        submitted = st.form_submit_button("Check Risk")

    if submitted:
        risk_result = get_risk_level(input_score, input_attendance)

        st.write("Student Name:", input_name)
        st.write("Score:", input_score)
        st.write("Attendance:", input_attendance)

        if risk_result == "Low Risk":
            st.success("Risk Level: Low Risk")
        elif risk_result == "Medium Risk":
            st.warning("Risk Level: Medium Risk")
        else:
            st.error("Risk Level: High Risk")

# About page
else:
    st.title("About")
    st.write("This app is part of Lab 02.")
    st.write("Course: Web App Development for Data Science")
    st.write("Project Theme: EduRisk Analytics")
    st.write("Topic: Streamlit Interactive Dashboard")
    st.info("Ethics Reminder: Risk prediction should support students, not punish them.")