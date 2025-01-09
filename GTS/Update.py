import streamlit as st
from services.thesis_ser import ThesisService
from services.university_ser import UniversityService
from services.institute_ser import InstituteService
from services.person_ser import PersonService

university_service = UniversityService()

def show_university_section():
    st.header("University Management")
    university_service = UniversityService()
    
    with st.form("add_university"):
        st.subheader("Add New University")
        name = st.text_input("University Name")
        if st.form_submit_button("Add University"):
            university_service.create_university(name)
            st.success("University added successfully!")
            st.rerun()
    
    universities = university_service.get_all_universities()
    if universities:
        st.subheader("Universities")
        for univ in universities:
            with st.container():
                col1, col2, col3 = st.columns([3,1,1])
                
                with col1:
                    if 'editing_university' in st.session_state and st.session_state.editing_university == univ['university_id']:
                        new_name = st.text_input(
                            "Edit Name", 
                            value=univ['name'],
                            key=f"edit_input_{univ['university_id']}"
                        )
                        col4, col5 = st.columns([1,1])
                        with col4:
                            if st.button("Save", key=f"save_{univ['university_id']}"):
                                try:
                                    university_service.update_university(univ['university_id'], new_name)
                                    st.success("University updated successfully!")
                                    st.session_state.editing_university = None
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating university: {str(e)}")
                        with col5:
                            if st.button("Cancel", key=f"cancel_{univ['university_id']}"):
                                st.session_state.editing_university = None
                                st.rerun()
                    else:
                        st.write(f"{univ['name']}")
                
                with col2:
                    if not ('editing_university' in st.session_state and 
                           st.session_state.editing_university == univ['university_id']):
                        if st.button("Edit", key=f"edit_{univ['university_id']}"):
                            st.session_state.editing_university = univ['university_id']
                            st.rerun()
                
                with col3:
                    if st.button("Delete", key=f"del_{univ['university_id']}"):
                        try:
                            university_service.delete_university(univ['university_id'])
                            st.success("University deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting university: {str(e)}")

def show_institute_section():
    st.header("Institute Management")
    institute_service = InstituteService()
    university_service = UniversityService()
    
    with st.form("add_institute"):
        st.subheader("Add New Institute")
        name = st.text_input("Institute Name")
        university = st.selectbox("Select University", 
            options=[u['name'] for u in university_service.get_all_universities()])
        if st.form_submit_button("Add Institute"):
            university_id = next(u['university_id'] 
                for u in university_service.get_all_universities() 
                if u['name'] == university)
            institute_service.create_institute(name, university_id)
            st.success("Institute added successfully!")
            st.rerun()
    
    institutes = institute_service.get_all_institutes()
    if institutes:
        st.subheader("Institutes")
        for institute in institutes:
            with st.container():
                col1, col2, col3, col4 = st.columns([3,2,1,1])
                
                with col1:
                    if 'editing_institute' in st.session_state and st.session_state.editing_institute == institute['institute_id']:
                        new_name = st.text_input("New Name", institute['name'], key=f"edit_institute_{institute['institute_id']}")
                        universities = university_service.get_all_universities()
                        university_options = {uni['name']: uni['university_id'] for uni in universities}
                        selected_university = st.selectbox(
                            "University",
                            options=list(university_options.keys()),
                            index=list(university_options.keys()).index(next((uni['name'] for uni in universities if uni['university_id'] == institute['university_id']), list(university_options.keys())[0])),
                            key=f"edit_institute_uni_{institute['institute_id']}"
                        )
                    else:
                        st.write(institute['name'])

                with col2:
                    if 'editing_institute' not in st.session_state or st.session_state.editing_institute != institute['institute_id']:
                        university = university_service.get_university_by_id(institute['university_id'])
                        st.write(university['name'] if university else "N/A")

                with col3:
                    if st.button("Edit", key=f"edit_btn_institute_{institute['institute_id']}"):
                        st.session_state.editing_institute = institute['institute_id']
                        st.rerun()

                with col4:
                    if 'editing_institute' in st.session_state and st.session_state.editing_institute == institute['institute_id']:
                        if st.button("Save", key=f"save_institute_{institute['institute_id']}"):
                            institute_service.update_institute(
                                institute['institute_id'],
                                new_name,
                                university_options[selected_university]
                            )
                            st.session_state.pop('editing_institute')
                            st.success("Institute updated successfully!")
                            st.rerun()
                    else:
                        if st.button("Delete", key=f"delete_institute_{institute['institute_id']}"):
                            institute_service.delete_institute(institute['institute_id'])
                            st.success("Institute deleted successfully!")
                            st.rerun()

def show_person_section():
    st.header("Person Management")
    person_service = PersonService()
    
    with st.form("add_person"):
        st.subheader("Add New Person")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Add Person"):
            person_service.create_person(name, surname, password)
            st.success("Person added successfully!")
            st.rerun()
    
    persons = person_service.get_all_persons()
    if persons:
        st.subheader("People")
        for person in persons:
            with st.container():
                col1, col2, col3 = st.columns([3,1,1])
                
                with col1:
                    if 'editing_person' in st.session_state and st.session_state.editing_person == person['person_id']:
                        new_name = st.text_input(
                            "Edit Name", 
                            value=person['name'],
                            key=f"edit_name_{person['person_id']}"
                        )
                        new_surname = st.text_input(
                            "Edit Surname", 
                            value=person['surname'],
                            key=f"edit_surname_{person['person_id']}"
                        )
                        col4, col5 = st.columns([1,1])
                        with col4:
                            if st.button("Save", key=f"save_{person['person_id']}"):
                                try:
                                    person_service.update_person(person['person_id'], new_name, new_surname)
                                    st.success("Person updated successfully!")
                                    st.session_state.editing_person = None
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Error updating person: {str(e)}")
                        with col5:
                            if st.button("Cancel", key=f"cancel_{person['person_id']}"):
                                st.session_state.editing_person = None
                                st.rerun()
                    else:
                        st.write(f"{person['name']} {person['surname']}")
                
                with col2:
                    if not ('editing_person' in st.session_state and 
                           st.session_state.editing_person == person['person_id']):
                        if st.button("Edit", key=f"edit_{person['person_id']}"):
                            st.session_state.editing_person = person['person_id']
                            st.rerun()
                
                with col3:
                    if st.button("Delete", key=f"del_{person['person_id']}"):
                        try:
                            person_service.delete_person(person['person_id'])
                            st.success("Person deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error deleting person: {str(e)}")

def main():
    st.title("Graduate Thesis System")
    
    tabs = [ "Universities", "Institutes", "People"]
    selected_tab = st.sidebar.selectbox("Select Section", tabs)
    
   
    if selected_tab == "Universities":
        show_university_section()
    elif selected_tab == "Institutes":
        show_institute_section()
    elif selected_tab == "People":
        show_person_section()

if __name__ == "__main__":
    main()