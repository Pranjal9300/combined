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

def filter_and_blank_timetable_by_subjects(timetable, selected_subjects):
    for index, row in timetable.iterrows():
        for col in timetable.columns[1:]:  # Skip the first column (time slot)
            cell_value = str(row[col]).strip()

            # Remove content within brackets and the brackets themselves
            cell_value = re.sub(r'\(.*?\)', '', cell_value).strip()

            # Identify subjects separated by '/'
            subjects_in_cell = [sub.strip() for sub in cell_value.split('/')]

            # If cell value does not match any of the selected subjects, blank it out
            if not any(sub in subjects_in_cell for sub in selected_subjects):
                timetable.at[index, col] = ""

    return timetable

def generate_timetable(timetable_file, selected_section, selected_subjects):
    # Load the timetable from the uploaded Excel file
    timetable_df = pd.read_excel(timetable_file, sheet_name="MBA 2023-25_3RD SEMESTER")

    # Filter timetable based on section and subjects
    filtered_timetable = timetable_df[timetable_df['Section'] == selected_section]

    # Apply subject filtering
    filtered_timetable = filter_and_blank_timetable_by_subjects(filtered_timetable, selected_subjects)

    return filtered_timetable

def main():
    st.title("Timetable and Profile Management")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    pages = st.sidebar.radio("Go to", ["Create/Edit Profile", "Generate Timetable"])

    if pages == "Create/Edit Profile":
        st.subheader("Create or Edit Profile")
        action = st.radio("Choose action", ["Create Profile", "Edit/Delete Profile"])

        if action == "Create Profile":
            st.write("Fill in the details to create a new profile:")
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

        elif action == "Edit/Delete Profile":
            st.write("Enter the enrollment number to search for a profile:")
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

    elif pages == "Generate Timetable":
        st.subheader("Generate Your Timetable")
        uploaded_file = st.file_uploader("Upload your timetable Excel file", type=["xlsx"])

        if uploaded_file:
            selected_section = st.selectbox("Select your Section", ["A", "B", "C"])

            if selected_section:
                st.subheader("Select Your Subjects")
                # Combine course title and abbreviation for selection
                subjects = [sub for sub in compulsory_subjects] + \
                           [sub for sub in general_electives_1] + \
                           [sub for sub in general_electives_2] + \
                           [sub for sub in major_sectors["Sales and Marketing"]] + \
                           [sub for sub in major_sectors["Finance"]] + \
                           [sub for sub in major_sectors["Business Analytics and Operations"]] + \
                           [sub for sub in major_sectors["Media"]] + \
                           [sub for sub in major_sectors["HR"]] + \
                           [sub for sub in major_sectors["Logistics & Supply Chain"]] + \
                           [sub for sub in additional_subjects]

                selected_subjects = st.multiselect("Subjects", subjects)

                if selected_subjects:
                    # Extract just the abbreviations to filter the timetable
                    selected_abbreviations = [sub.split('(')[-1].replace(')', '').strip() for sub in selected_subjects]

                    # Generate and display the filtered timetable
                    personal_timetable = generate_timetable(uploaded_file, selected_section, selected_abbreviations)
                    st.subheader("Your Personal Timetable")
                    st.dataframe(personal_timetable)
        else:
            st.info("Please upload a timetable file.")

if __name__ == "__main__":
    main()
