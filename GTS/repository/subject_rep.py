from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from entities.entities import Subject

class SubjectRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_subject(self, name: str) -> dict:
        try:
            subject = Subject(name=name)
            self.session.add(subject)
            self.session.flush()
            return self._to_dict(subject)
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error creating subject: {str(e)}")

    def get_all_subjects(self) -> list[dict]:
        subjects = self.session.query(Subject).all()
        return [self._to_dict(s) for s in subjects]

    def get_subject_by_id(self, subject_id: int) -> dict:
        subject = self.session.query(Subject).filter(Subject.subject_id == subject_id).first()
        return self._to_dict(subject) if subject else None

    def update_subject(self, subject_id: int, name: str) -> dict:
        try:
            subject = self.session.query(Subject).filter(Subject.subject_id == subject_id).first()
            if subject:
                subject.name = name
                self.session.flush()
                return self._to_dict(subject)
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error updating subject: {str(e)}")

    def delete_subject(self, subject_id: int) -> bool:
        try:
            subject = self.session.query(Subject).filter(Subject.subject_id == subject_id).first()
            if subject:
                self.session.delete(subject)
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error deleting subject: {str(e)}")

    def _to_dict(self, subject: Subject) -> dict:
        return {
            'subject_id': subject.subject_id,
            'name': subject.name
        }