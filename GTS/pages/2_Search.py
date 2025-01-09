import streamlit as st
from datetime import date
from services.thesis_ser import ThesisService
from services.person_ser import PersonService
from services.university_ser import UniversityService
from services.institute_ser import InstituteService
from services.subject_ser import SubjectService
from entities.entities import ThesisType, Language

def show_search_form():
    st.title("Thesis Search")
    
    # Initialize services
    thesis_service = ThesisService()
    person_service = PersonService()
    university_service = UniversityService()
    institute_service = InstituteService()
    subject_service = SubjectService()

    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title_search = st.text_input("Title Contains")
            abstract_search = st.text_input("Abstract Contains")
            keyword_search = st.text_input("Keyword Contains")
            
            year_start = st.number_input("From Year", min_value=1920, 
                                       max_value=date.today().year, 
                                       value=1920)
            year_end = st.number_input("To Year", min_value=1920, 
                                     max_value=date.today().year, 
                                     value=date.today().year)

        with col2:
            thesis_type = st.selectbox("Thesis Type", 
                                     options=["All"] + [t.value for t in ThesisType])
            language = st.selectbox("Language", 
                                  options=["All"] + [l.value for l in Language])
            
        
            persons = person_service.get_all_persons()
            person_options = {f"{p['name']} {p['surname']}": p['person_id'] 
                            for p in persons}
            
            author_search = st.selectbox("Author", 
                                       options=["All"] + list(person_options.keys()))
            supervisor_search = st.selectbox("Supervisor", 
                                          options=["All"] + list(person_options.keys()))

        submitted = st.form_submit_button("Search")

    if submitted:
        search_criteria = {
            "title": title_search if title_search else None,
            "abstract": abstract_search if abstract_search else None,
            "keyword": keyword_search if keyword_search else None,
            "year_start": year_start,
            "year_end": year_end,
            "type": thesis_type if thesis_type != "All" else None,
            "language": language if language != "All" else None,
            "author_id": person_options[author_search] if author_search != "All" else None,
            "supervisor_id": person_options[supervisor_search] 
                           if supervisor_search != "All" else None
        }

        
        results = thesis_service.search_theses(search_criteria)
        
        if results:
            st.subheader(f"Found {len(results)} theses")
            
            sort_by = st.selectbox("Sort by", 
                                 ["Year (Newest)", "Year (Oldest)", "Title (A-Z)", 
                                  "Title (Z-A)"])
            
            if sort_by == "Year (Newest)":
                results.sort(key=lambda x: x['year'], reverse=True)
            elif sort_by == "Year (Oldest)":
                results.sort(key=lambda x: x['year'])
            elif sort_by == "Title (A-Z)":
                results.sort(key=lambda x: x['title'])
            else:
                results.sort(key=lambda x: x['title'], reverse=True)

            for thesis in results:
                with st.expander(f"{thesis['title']} ({thesis['year']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Author:** {thesis['author_name']}")
                        st.write(f"**Supervisor:** {thesis['supervisor_name']}")
                        st.write(f"**Type:** {thesis['type']}")
                        st.write(f"**Language:** {thesis['language']}")
                    with col2:
                        st.write(f"**University:** {thesis['university_name']}")
                        st.write(f"**Institute:** {thesis['institute_name']}")
                        st.write(f"**Year:** {thesis['year']}")
                        st.write(f"**Pages:** {thesis['number_of_pages']}")
                    
                    st.write("**Abstract:**")
                    st.write(thesis['abstract'])
                    
                    if thesis.get('keywords'):
                        st.write("**Keywords:**", ", ".join(thesis['keywords']))
                    
                    if thesis.get('subjects'):
                        st.write("**Subjects:**", ", ".join(thesis['subjects']))
        else:
            st.info("No theses found matching your criteria")

if __name__ == "__main__":
    show_search_form()