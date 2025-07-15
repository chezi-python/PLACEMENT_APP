import streamlit as st
import mysql.connector
import pandas as pd


class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sheela@1981",
            port=3306,
            database="faker_db"
        )

    def fetch(self, query, params=None):
        return pd.read_sql(query, self.conn, params=params)

    def close(self):
        self.conn.close()



class StudentManager:
    def __init__(self, db: Database):
        self.db = db

    def get_eligible_students(self, prob_thresh, soft_skill_thresh, cert_thresh, proj_thresh):
        query = f"""
            SELECT s.student_id, s.name, s.course_batch,
                   p.problems_solved, p.certifications_earned, p.latest_project_score,
                   ss.communication, ss.teamwork, ss.presentation, ss.leadership,
                   ss.critical_thinking, ss.interpersonal_skills
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            WHERE p.problems_solved >= {prob_thresh}
              AND (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6 >= {soft_skill_thresh}
              AND p.certifications_earned >= {cert_thresh}
              AND p.latest_project_score >= {proj_thresh}
        """
        return self.db.fetch(query)

    def get_full_details(self, student_name):
        query = """
            SELECT s.student_id, s.name, s.age, s.gender, s.email, s.phone, s.city,
                   s.course_batch, s.enrollment_year, s.graduation_year,
                   p.language, p.problems_solved, p.assessments_completed,
                   p.certifications_earned, p.latest_project_score, p.mini_projects,
                   ss.communication, ss.teamwork, ss.presentation, ss.leadership,
                   ss.critical_thinking, ss.interpersonal_skills,
                   pl.placement_status, pl.company_name, pl.placement_package,
                   pl.mock_interview_score, pl.interview_rounds_cleared
            FROM Students s
            JOIN Programming p ON s.student_id = p.student_id
            JOIN SoftSkills ss ON s.student_id = ss.student_id
            LEFT JOIN Placements pl ON s.student_id = pl.student_id
            WHERE s.name = %s
            LIMIT 1;
        """
        return self.db.fetch(query, [student_name])



class InsightManager:
    def __init__(self, db: Database):
        self.db = db
        self.query_map = {
            "Average Programming Performance per Batch": """
                SELECT course_batch, AVG(problems_solved) AS avg_problems
                FROM Students s
                JOIN Programming p ON s.student_id = p.student_id
                GROUP BY course_batch;
            """,
            "Top 5 Students Ready for Placement": """
                SELECT s.student_id, s.name, pl.placement_status, pl.mock_interview_score
                FROM Students s
                JOIN Placements pl ON s.student_id = pl.student_id
                WHERE pl.placement_status = 'Ready'
                ORDER BY pl.mock_interview_score DESC
                LIMIT 5;
            """,
            "Soft Skills Score Distribution": """
                SELECT
                    ROUND((communication + teamwork + presentation + leadership + critical_thinking + interpersonal_skills)/6, 2) AS avg_soft_skill,
                    COUNT(*) AS student_count
                FROM SoftSkills
                GROUP BY avg_soft_skill
                ORDER BY avg_soft_skill DESC;
            """,
            "Students with Placement Package > 100K": """
                SELECT s.student_id, s.name, pl.company_name, pl.placement_package
                FROM Students s
                JOIN Placements pl ON s.student_id = pl.student_id
                WHERE pl.placement_status = 'Placed' AND pl.placement_package > 100000;
            """,
            "Students with More than 3 Certifications": """
                SELECT s.student_id, s.name, p.certifications_earned
                FROM Students s
                JOIN Programming p ON s.student_id = p.student_id
                WHERE p.certifications_earned > 3;
            """,
            "Average Mock Interview Scores per Batch": """
                SELECT course_batch, AVG(pl.mock_interview_score) AS avg_mock_score
                FROM Students s
                JOIN Placements pl ON s.student_id = pl.student_id
                GROUP BY course_batch;
            """,
            "Student Count by City": """
                SELECT city, COUNT(*) AS total_students
                FROM Students
                GROUP BY city
                ORDER BY total_students DESC;
            """,
            "Students with Most Mini Projects": """
                SELECT s.student_id, s.name, p.mini_projects
                FROM Students s
                JOIN Programming p ON s.student_id = p.student_id
                ORDER BY p.mini_projects DESC
                LIMIT 5;
            """,
            "Placement Status Summary": """
                SELECT placement_status, COUNT(*) AS count
                FROM Placements
                GROUP BY placement_status;
            """,
            "Top Overall Performer (Soft Skills + Project Score)": """
                SELECT s.student_id, s.name,
                       ROUND((ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6, 2) AS avg_soft,
                       p.latest_project_score,
                       ROUND((p.latest_project_score + (ss.communication + ss.teamwork + ss.presentation + ss.leadership + ss.critical_thinking + ss.interpersonal_skills)/6)/2, 2) AS total_score
                FROM Students s
                JOIN SoftSkills ss ON s.student_id = ss.student_id
                JOIN Programming p ON s.student_id = p.student_id
                ORDER BY total_score DESC
                LIMIT 1;
            """
        }

    def get_insight(self, key):
        return self.db.fetch(self.query_map[key])



st.set_page_config(page_title="Placement Eligibility App", layout="wide")
st.title("🎓 Placement Eligibility App  ")


db = Database()
student_mgr = StudentManager(db)
insight_mgr = InsightManager(db)

if 'eligible_students_df' not in st.session_state:
    st.session_state.eligible_students_df = pd.DataFrame()

if 'selected_eligible_student_name' not in st.session_state:
    st.session_state.selected_eligible_student_name = None

tab1, tab2, tab3, tab4 = st.tabs(["1. Eligibility Criteria", "2. Eligible Students", "3. Student Details", "4. Data Insights"])

#  TAB 1 
with tab1:
    st.header("Set Eligibility Criteria")

    prob = st.number_input("Minimum Problems Solved", 0, 500, 50, 10)
    soft = st.number_input("Minimum Soft Skills Score (Average)", 0, 100, 75, 5)
    cert = st.number_input("Minimum Certifications Earned", 0, 5, 1, 1)
    proj = st.number_input("Minimum Latest Project Score", 0, 100, 60, 5)

    if st.button("Find Eligible Students"):
        st.session_state.eligible_students_df = student_mgr.get_eligible_students(prob, soft, cert, proj)
        if st.session_state.eligible_students_df.empty:
            st.info("No students meet the specified criteria.")
        else:
            st.success("Eligible students found! Check the next tab.")

# TAB 2 ---
with tab2:
    st.header("✅ Eligible Students")
    if not st.session_state.eligible_students_df.empty:
        st.dataframe(st.session_state.eligible_students_df.sort_values(by=["problems_solved", "latest_project_score"], ascending=[False, False]))
    else:
        st.info("No eligible students yet.Again Run the eligibility filter in the first tab.")

# Tab 3 ---
with tab3:
    st.header(" Student Full Details")

    if not st.session_state.eligible_students_df.empty:
        student_name = st.selectbox("Select Student", st.session_state.eligible_students_df["name"])
        st.session_state.selected_eligible_student_name = student_name

        if st.button("Show Student Details"):
            detail = student_mgr.get_full_details(student_name)
            if not detail.empty:
                col1, col2 = st.columns(2)
                #st.subheader(f"📋 Full Profile: {student_name}")

                with col1:
                    st.markdown("General")
                    st.write(detail[["name","student_id", "age", "gender", "email", "phone", "city", "course_batch", "enrollment_year", "graduation_year"]].T)

                    st.markdown("Soft Skills")
                    st.write(detail[["communication", "teamwork", "presentation", "leadership", "critical_thinking", "interpersonal_skills"]].T)

                with col2:
                    st.markdown(" Programming")
                    st.write(detail[["language", "problems_solved", "assessments_completed", "certifications_earned", "latest_project_score", "mini_projects"]].T)

                    st.markdown("Placement")
                    st.write(detail[["placement_status", "company_name", "placement_package", "mock_interview_score", "interview_rounds_cleared"]].T)
            else:
                st.warning("No details found.")

# TAB 4 ---
with tab4:
    st.header("📊 Data Insights")

    selected_query = st.selectbox("Choose an Insight", list(insight_mgr.query_map.keys()))

    if selected_query:
        result = insight_mgr.get_insight(selected_query)
        st.markdown(f"### {selected_query}")
        st.dataframe(result)


db.close()



