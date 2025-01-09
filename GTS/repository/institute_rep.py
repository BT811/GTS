from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from entities.entities import Institute

class InstituteRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_institute(self, name: str, university_id: int) -> dict:
        try:
            institute = Institute(name=name, university_id=university_id)
            self.session.add(institute)
            self.session.flush()
            return self._to_dict(institute)
        except SQLAlchemyError as e:
            raise ValueError(f"Error creating institute: {str(e)}")

    def get_all_institutes(self) -> list[dict]:
        institutes = self.session.query(Institute).all()
        return [self._to_dict(i) for i in institutes]

    def get_institute_by_id(self, institute_id: int) -> dict:
        institute = self.session.query(Institute).filter(Institute.institute_id == institute_id).first()
        return self._to_dict(institute) if institute else None

    def get_institutes_by_university(self, university_id: int) -> list[dict]:
        institutes = self.session.query(Institute).filter(
            Institute.university_id == university_id
        ).all()
        return [self._to_dict(i) for i in institutes]

    def update_institute(self, institute_id: int, name: str, university_id: int) -> dict:
        institute = self.session.query(Institute).filter(Institute.institute_id == institute_id).first()
        if institute:
            institute.name = name
            institute.university_id = university_id
            return self._to_dict(institute)
        return None

    def delete_institute(self, institute_id: int) -> bool:
        institute = self.session.query(Institute).filter(Institute.institute_id == institute_id).first()
        if institute:
            self.session.delete(institute)
            return True
        return False

    def _to_dict(self, institute: Institute) -> dict:
        return {
            'institute_id': institute.institute_id,
            'name': institute.name,
            'university_id': institute.university_id
        }