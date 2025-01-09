from sqlalchemy.orm import Session, joinedload, aliased
from sqlalchemy import or_, and_
from entities.entities import Thesis, ThesisType, Language, Person, University, Institute, Keyword, Subject, ThesisSubject, CoSupervisorThesis
from typing import Dict, Any
from sqlalchemy.exc import SQLAlchemyError

class ThesisRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_thesis_by_id(self, thesis_id: int) -> dict:
        thesis = self.session.query(Thesis).filter(Thesis.thesis_id == thesis_id).first()
        if thesis:
            return {
                'thesis_id': thesis.thesis_id,
                'author_id': thesis.author_id,
                'supervisor_id': thesis.supervisor_id,
                'title': thesis.title,
                'abstract': thesis.abstract,
                'year': thesis.year,
                'type': ThesisType(thesis.type),
                'university_id': thesis.university_id,
                'institute_id': thesis.institute_id,
                'number_of_pages': thesis.number_of_pages,
                'language': Language(thesis.language),
                'submission_date': thesis.submission_date
            }
        return None

    def search_theses(self, criteria: Dict[str, Any]) -> list[dict]:
        Author = aliased(Person)
        Supervisor = aliased(Person)

        query = self.session.query(
            Thesis,
            Author,
            Supervisor,
            University,
            Institute
        ).join(
            Author, Thesis.author_id == Author.person_id
        ).join(
            Supervisor, Thesis.supervisor_id == Supervisor.person_id
        ).outerjoin(
            University, Thesis.university_id == University.university_id
        ).outerjoin(
            Institute, Thesis.institute_id == Institute.institute_id
        ).outerjoin(
            Keyword, Thesis.thesis_id == Keyword.thesis_id
        ).outerjoin(
            ThesisSubject, Thesis.thesis_id == ThesisSubject.thesis_id
        ).outerjoin(
            Subject, ThesisSubject.subject_id == Subject.subject_id
        )

        if criteria.get('title'):
            query = query.filter(Thesis.title.ilike(f"%{criteria['title']}%"))
        
        if criteria.get('abstract'):
            query = query.filter(Thesis.abstract.ilike(f"%{criteria['abstract']}%"))
            
        if criteria.get('keyword'):
            query = query.filter(Keyword.name.ilike(f"%{criteria['keyword']}%"))
            
        if criteria.get('year_start'):
            query = query.filter(Thesis.year >= criteria['year_start'])
            
        if criteria.get('year_end'):
            query = query.filter(Thesis.year <= criteria['year_end'])
            
        if criteria.get('type'):
            query = query.filter(Thesis.type == criteria['type'])
            
        if criteria.get('language'):
            query = query.filter(Thesis.language == criteria['language'])
            
        if criteria.get('author_id'):
            query = query.filter(Author.person_id == criteria['author_id'])
            
        if criteria.get('supervisor_id'):
            query = query.filter(Supervisor.person_id == criteria['supervisor_id'])

        results = query.all()
        return [self._to_dict_with_relations(result) for result in results]

    def _to_dict_with_relations(self, result) -> dict:
        thesis, author, supervisor, university, institute = result
        return {
            'thesis_id': thesis.thesis_id,
            'title': thesis.title,
            'abstract': thesis.abstract,
            'year': thesis.year,
            'type': thesis.type,
            'number_of_pages': thesis.number_of_pages,
            'language': thesis.language,
            'submission_date': thesis.submission_date,
            'author_name': f"{author.name} {author.surname}",
            'supervisor_name': f"{supervisor.name} {supervisor.surname}",
            'university_name': university.name if university else None,
            'institute_name': institute.name if institute else None,
            'keywords': [],   
            'subjects': []   
        }

    def create_thesis(self, thesis_data: Dict[str, Any]) -> dict:
        try:
            thesis = Thesis(
                author_id=thesis_data['author_id'],
                supervisor_id=thesis_data['supervisor_id'],
                title=thesis_data['title'],
                abstract=thesis_data['abstract'],
                year=thesis_data['year'],
                type=thesis_data['type'],
                university_id=thesis_data.get('university_id'),
                institute_id=thesis_data.get('institute_id'),
                number_of_pages=thesis_data['number_of_pages'],
                language=thesis_data['language'],
                submission_date=thesis_data['submission_date']
            )
            
            self.session.add(thesis)
            self.session.flush()
            thesis_id = thesis.thesis_id

            if thesis_data.get('co_supervisor_ids'):
                for co_supervisor_id in thesis_data['co_supervisor_ids']:
                    co_supervisor = CoSupervisorThesis(
                        thesis_id=thesis_id,
                        person_id=co_supervisor_id
                    )
                    self.session.add(co_supervisor)

            if thesis_data.get('subject_ids'):
                for subject_id in thesis_data['subject_ids']:
                    thesis_subject = ThesisSubject(
                        thesis_id=thesis_id,
                        subject_id=subject_id
                    )
                    self.session.add(thesis_subject)

            if thesis_data.get('keywords'):
                for keyword in thesis_data['keywords']:
                    keyword_entity = Keyword(
                        thesis_id=thesis_id,
                        name=keyword
                    )
                    self.session.add(keyword_entity)

            return self.get_thesis_by_id(thesis_id)

        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error creating thesis: {str(e)}")