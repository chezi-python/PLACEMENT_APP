# PLACEMENT_APP

🎓 Placement Eligibility Data App
This Streamlit application provides a comprehensive tool for managing and analyzing student placement eligibility data. It allows users to define custom criteria for identifying eligible students, view filtered student lists, access detailed profiles of individual students, and explore various data insights through pre-defined SQL queries.

✨ Features
Eligibility Criteria Input (Tab 1):

Set minimum thresholds for "Problems Solved", "Soft Skills Score (Average)", "Certifications Earned", and "Latest Project Score".

Find and filter students based on these criteria.

Filtered Eligible Students (Tab 2):

Displays a table of students who meet the specified eligibility criteria.

The table is ordered by programming performance metrics for easy review.

Selected Student Full Details (Tab 3):

Allows selection of an eligible student from a dropdown.

Displays a comprehensive profile including general information, programming performance, soft skills, and placement details (if available).

Details are shown upon clicking a "Show Student Details" button.

Data Insights - SQL Queries (Tab 4):

Provides a selection of pre-defined SQL queries to gain various insights into the student data (e.g., average performance per batch, placement status summaries, top performers).


Students: Contains general student information (student_id, name, age, gender, email, phone, city, course_batch, enrollment_year, graduation_year).

Programming: Contains programming-related metrics (student_id, language, problems_solved, assessments_completed, certifications_earned, latest_project_score, mini_projects).

SoftSkills: Contains soft skill scores (student_id, communication, teamwork, presentation, leadership, critical_thinking, interpersonal_skills).

Placements: Contains placement-related data (student_id, placement_status, company_name, placement_package, mock_interview_score, interview_rounds_cleared).


💡 Usage
The application is structured into four tabs for easy navigation:

Eligibility Criteria:

Use the number input fields to set your desired minimum thresholds for Problems Solved, Soft Skills Score (Average), Certifications Earned, and Latest Project Score.

Click the "Find Eligible Students" button.

A message will confirm if eligible students were found or if no students matched the criteria.

Eligible Students:

After setting criteria and finding eligible students in Tab 1, navigate to this tab.

A table displaying all students who meet your criteria will be shown, ordered by their programming performance.

Student Details:

Select a student from the "Select an eligible student to view full details" dropdown. This dropdown will only list students found in Tab 2.

Click the "Show Student Details" button to display the selected student's comprehensive profile, including general, programming, soft skills, and placement information, organized into two columns.

Data Insights:

Choose a pre-defined SQL query from the "Select a data insight to view" dropdown.

The results of the selected query will be displayed in a DataFrame.
