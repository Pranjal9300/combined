import streamlit as st
import pandas as pd

# Predefined subjects and major sectors
compulsory_subjects = ["Innovation, Entrepreneurship and Start-ups (IES)", "Know yourself (KY)", "Professional Ethics (PE)"]
general_electives_1 = ["Bibliophiles (Bibl)", "Psychology in Business (PB-A)"]
general_electives_2 = ["International Business (IB)", "Project Management (PM)", "E-Business (E.Bus)"]
major_sectors = {
    "Sales and Marketing": ["Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)"],
    "Finance": ["Financial Statement Analysis (FSA)", "Business Valuation (BussV)", "Security and Portfolio Management (SPM)"],
    "Business Analytics and Operations": ["Programming for Analytics (PA)", "Data Mining and Visualization (DMV)", "AI and Machine Learning (AIML)"],
    "Media": ["Digital Media (DM)", "Media Production and Consumption (MPC)", "Media Research Tools and Analytics (MRTA)"],
    "HR": ["Performance Management System (PMS)", "Talent Acquisition (TA)", "Learnings & Development (L&D)"],
    "Logistics & Supply Chain": ["Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)"]
}
additional_subjects = [
    "Consumer Behaviour (CB)", "Integrated Marketing Communication (IMC)", "Sales & Distribution Management (S&DM)",
    "Marketing Analytics (Man)", "Strategic Brand Management (SBM)", "Financial Statement Analysis (FSA)",
    "Business Valuation (BussV)", "Security and Portfolio Management (SPM)", "International Finance (IF)",
    "Management of Banks (MoB)", "Programming for Analytics (PA)", "Text Mining and Sentiment Analytics (TM&SA)",
    "Data Mining and Visualization (DMV)", "Analytics for Service Operations (ASO)", "AI and Machine Learning (AIML)",
    "Digital Media (DM)", "Media Production and Consumption (MPC)", "Media and Sports Industry (MSI)",
    "Media Research Tools and Analytics (MRTA)", "Media Cost Management & Control (MCMC)", "Performance Management System (PMS)",
    "Talent Acquisition (TA)", "Learnings & Development (L&D)", "Compensation & Reward Management (C&RM)",
    "Purchasing & Inventory Management (P&IM)", "Supply Chain Management (SCM)", "Transportation & Distribution Management (TDM)",
    "Warehousing & Distribution Facilities Management (W&DFM)"
]

# Initialize profiles dictionary
if "profiles" not in st.session_state:
    st.session_state["profiles"] = {}

def generate_timetable(uploaded_file, student_id):
    # Load the timetable file
    timetable_df = pd.read_excel(uploaded_file, sheet_name="MBA 2023-25_3RD SEMESTER")
    
    # Get the profile of the student
    profile = st.session_state["profiles"].get(student_id)
    
    if not profile:
        st.error("Profile not found for this enrollment number.")
        return None

    selected_section = profile["section"]
    selected_abbreviations = [
        profile["elective_1"],
        profile["elective_2"]
    ]
    
    major_sector_subjects = major_sectors[profile["major_sector"]]
    selected_abbreviations.extend(major_sector_subjects)
    
    selected_abbreviations.append(profile["additional_subject"])

    # Filter the timetable for the selected section
    filtered_timetable = timetable_df[timetable_df['Section'] == selected_section]

    for index, row in filtered_timetable.iterrows():
        for col in filtered_timetable.columns[1:]:
            cell_value = str(row[col]).strip()
            # Remove content in brackets
            cell_value = re.sub(r'\[.*?\]', '', cell_value).strip()
            # Split by '/' to handle multiple subjects
            subjects = [sub.strip() for sub in cell_value.split('/')]

            if not any(sub in selected_abbreviations for sub in subjects):
                filtered_timetable.at[index, col] = ""

    return filtered_timetable

def main():
    st.title("Personal Timetable Generator")

    # Upload timetable file
    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

    # Create or Edit Profile
    st.sidebar.title("Profile Management")
    pages = st.sidebar.radio("Go to", ["Create Profile", "Edit/Delete Profile"])

    if pages == "Create Profile":
        st.title("Create Profile")
        name = st.text_input("Enter your name")
        enrollment_no = st.text_input("Enter your enrollment number")
        section = st.selectbox("Select your section", ["A", "B", "C"])

        st.subheader("Compulsory Subjects")
        for subject in compulsory_subjects:
            st.checkbox(subject, value=True, disabled=True)

        st.subheader("General Electives 1")
        elective_1 = st.selectbox("Choose one", general_electives_1)

        st.subheader("General Electives 2")
        elective_2 = st.selectbox("Choose one", general_electives_2)

        st.subheader("Major Sector")
        major_sector = st.selectbox("Choose a sector", list(major_sectors.keys()))
        for subject in major_sectors[major_sector]:
            st.checkbox(subject, value=True, disabled=True)

        st.subheader("Additional Subject")
        additional_subject = st.selectbox("Choose one", additional_subjects)

        if st.button("Save Profile"):
            st.session_state["profiles"][enrollment_no] = {
                "name": name,
                "section": section,
                "elective_1": elective_1,
                "elective_2": elective_2,
                "major_sector": major_sector,
                "additional_subject": additional_subject
            }
            st.success("Profile saved successfully!")

    elif pages == "Edit/Delete Profile":
        st.title("Edit or Delete Profile")
        enrollment_no = st.text_input("Enter your enrollment number to search")

        if enrollment_no in st.session_state["profiles"]:
            profile = st.session_state["profiles"][enrollment_no]
            st.write(f"Name: {profile['name']}")
            st.write(f"Section: {profile['section']}")
            st.write(f"Elective 1: {profile['elective_1']}")
            st.write(f"Elective 2: {profile['elective_2']}")
            st.write(f"Major Sector: {profile['major_sector']}")
            st.write(f"Additional Subject: {profile['additional_subject']}")

            if st.button("Delete Profile"):
                del st.session_state["profiles"][enrollment_no]
                st.success("Profile deleted successfully!")

            if st.button("Edit Profile"):
                st.session_state["profiles"][enrollment_no] = {
                    "name": st.text_input("Enter your name", value=profile['name']),
                    "section": st.selectbox("Select your section", ["A", "B", "C"], index=["A", "B", "C"].index(profile['section'])),
                    "elective_1": st.selectbox("Choose one", general_electives_1, index=general_electives_1.index(profile['elective_1'])),
                    "elective_2": st.selectbox("Choose one", general_electives_2, index=general_electives_2.index(profile['elective_2'])),
                    "major_sector": st.selectbox("Choose a sector", list(major_sectors.keys()), index=list(major_sectors.keys()).index(profile['major_sector'])),
                    "additional_subject": st.selectbox("Choose one", additional_subjects, index=additional_subjects.index(profile['additional_subject']))
                }
                st.success("Profile edited successfully!")

        else:
            st.info("No profile found for this enrollment number.")

    if uploaded_file:
        student_id = st.text_input("Enter your enrollment number to generate timetable")
        if student_id:
            personal_timetable = generate_timetable(uploaded_file, student_id)
            if personal_timetable is not None:
                st.subheader("Your Personal Timetable")
                st.dataframe(personal_timetable)
        else:
            st.info("Please enter an enrollment number.")

if __name__ == "__main__":
    main()
