import streamlit as st
from datetime import date
from services.person_ser import PersonService
from services.university_ser import UniversityService
from services.institute_ser import InstituteService
from services.subject_ser import SubjectService
from services.thesis_ser import ThesisService
from entities.entities import ThesisType, Language

def show_thesis_form():
    st.title("Create New Thesis")

    person_service = PersonService()
    university_service = UniversityService()
    institute_service = InstituteService()
    subject_service = SubjectService()
    thesis_service = ThesisService()

    st.subheader("Basic Information")
    title = st.text_input("Thesis Title", max_chars=500)
    abstract = st.text_area("Abstract")
    year = st.number_input("Year", min_value=1900, max_value=date.today().year, value=date.today().year)
    number_of_pages = st.number_input("Number of Pages", min_value=1)
    thesis_type = st.selectbox("Thesis Type", options=[t.value for t in ThesisType])
    language = st.selectbox("Language", options=[l.value for l in Language])
    submission_date = st.date_input("Submission Date", value=date.today())

    st.subheader("Author Information")
    persons = person_service.get_all_persons()
    person_options = {f"{p['name']} {p['surname']}": p['person_id'] for p in persons}
    
    selected_author = st.selectbox("Select Author", options=list(person_options.keys()))
    selected_supervisor = st.selectbox("Select Supervisor (Required)", options=list(person_options.keys()))
    selected_co_supervisors = st.multiselect("Select Co-Supervisors (Optional)", 
                                           options=[k for k in person_options.keys() if k != selected_supervisor])

    st.subheader("Institution Information")
    universities = university_service.get_all_universities()
    university_options = {u['name']: u['university_id'] for u in universities}
    selected_university = st.selectbox("Select University", options=list(university_options.keys()))

    institute_options = {}
    selected_institute = None
    if selected_university:
        institutes = institute_service.get_institutes_by_university(
            university_options[selected_university])
        institute_options = {i['name']: i['institute_id'] for i in institutes}
        selected_institute = st.selectbox("Select Institute", options=list(institute_options.keys()))

    st.subheader("Subjects and Keywords")
    subjects = subject_service.get_all_subjects()
    subject_options = {s['name']: s['subject_id'] for s in subjects}
    selected_subjects = st.multiselect("Select Subjects (At least one required)", 
                                     options=list(subject_options.keys()))

    keywords = st.text_area("Enter Keywords (One per line)")
    keyword_list = [k.strip() for k in keywords.split('\n') if k.strip()]

    if st.button("Create Thesis"):
        try:
            if not (title and abstract and selected_author and 
                    selected_supervisor and selected_subjects):
                st.error("Please fill all required fields")
                return

            if selected_author == selected_supervisor:
                st.error("Author cannot be the supervisor")
                return
                
            if selected_author in selected_co_supervisors:
                st.error("Author cannot be a co-supervisor")
                return
                
            if selected_supervisor in selected_co_supervisors:
                st.error("Supervisor cannot be a co-supervisor")
                return

            thesis_data = {
                'title': title,
                'abstract': abstract,
                'year': year,
                'type': thesis_type,
                'number_of_pages': number_of_pages,
                'language': language,
                'submission_date': submission_date,
                'author_id': person_options[selected_author],
                'supervisor_id': person_options[selected_supervisor],
                'co_supervisor_ids': [person_options[cs] for cs in selected_co_supervisors],
                'university_id': university_options[selected_university],
                'institute_id': institute_options[selected_institute],
                'subject_ids': [subject_options[s] for s in selected_subjects],
                'keywords': keyword_list
            }

            thesis_service.create_thesis(thesis_data)
            st.success("Thesis created successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))
        except Exception as e:
            st.error(f"Error creating thesis: {str(e)}")

if __name__ == "__main__":
    show_thesis_form()