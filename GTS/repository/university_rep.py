from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from entities.entities import University

class UniversityRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_university(self, name: str) -> dict:
        try:
            university = University(name=name)
            self.session.add(university)
            self.session.flush()
            return {
                'university_id': university.university_id,
                'name': university.name
            }
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error creating university: {str(e)}")

    def get_all_universities(self) -> list[dict]:
        universities = self.session.query(University).all()
        return [
            {
                'university_id': u.university_id,
                'name': u.name
            }
            for u in universities
        ]

    def get_university_by_id(self, university_id: int) -> dict:
        university = self.session.query(University).filter(
            University.university_id == university_id
        ).first()
        if university:
            return {
                'university_id': university.university_id,
                'name': university.name
            }
        return None

    def update_university(self, university_id: int, name: str) -> dict:
        try:
            university = self.session.query(University).filter(
                University.university_id == university_id
            ).first()
            if university:
                university.name = name
                self.session.flush()
                return {
                    'university_id': university.university_id,
                    'name': university.name
                }
            raise ValueError(f"University with id {university_id} not found")
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error updating university: {str(e)}")

    def delete_university(self, university_id: int) -> bool:
        try:
            university = self.session.query(University).filter(
                University.university_id == university_id
            ).first()
            if university:
                self.session.delete(university)
                return True
            return False
        except SQLAlchemyError as e:
            self.session.rollback()
            raise ValueError(f"Error deleting university: {str(e)}")