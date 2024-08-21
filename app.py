import streamlit as st
import pandas as pd

# Predefined subjects
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

def load_excel(file):
    return pd.read_excel(file, sheet_name=None)

def get_section_timetable(timetable_sheet, section):
    section_start = {'A': 2, 'B': 16, 'C': 30}
    start_row = section_start.get(section)
    end_row = start_row + 12 if start_row is not None else None
    return timetable_sheet.iloc[start_row:end_row] if start_row is not None else None

def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:
            cell_value = str(row[col]).strip()
            if '(' in cell_value and ')' in cell_value:
                cell_value = cell_value.split('(')[0].strip()
            cell_value = cell_value.split('/')[0].strip()
            if not any(sub in cell_value for sub in selected_subjects):
                timetable.at[index, col] = ""
    return timetable

# Sidebar for navigation
st.sidebar.title("Navigation")
pages = st.sidebar.radio("Go to", ["Create/Edit Profile", "Timetable Filter"])

if pages == "Create/Edit Profile":
    st.title("Create or Edit Profile")
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

elif pages == "Timetable Filter":
    st.title("Timetable Filter")
    uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

    if uploaded_file:
        sheets = load_excel(uploaded_file)
        timetable_sheet = sheets.get("MBA 2023-25_3RD SEMESTER")

        enrollment_no = st.text_input("Enter your enrollment number to load profile")
        if enrollment_no in st.session_state["profiles"]:
            profile = st.session_state["profiles"][enrollment_no]
            selected_subjects = [profile['elective_1'], profile['elective_2']] + major_sectors[profile['major_sector']] + [profile['additional_subject']]
            section_timetable = get_section_timetable(timetable_sheet, profile["section"])

            if section_timetable is not None:
                personal_timetable = filter_and_blank_timetable_by_subjects(section_timetable, selected_subjects)
                st.subheader("Your Personal Timetable")
                st.dataframe(personal_timetable)
            else:
                st.error(f"Timetable for Section {profile['section']} not found.")
        else:
            st.warning("Profile not found. Please create a profile first.")

if __name__ == "__main__":
    main()
