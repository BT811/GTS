from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from entities.entities import Person

class PersonRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_person(self, name: str, surname: str, password: str) -> dict:
        try:
            person = Person(name=name, surname=surname, password=password)
            self.session.add(person)
            self.session.flush()
            return self._to_dict(person)
        except SQLAlchemyError as e:
            raise ValueError(f"Error creating person: {str(e)}")

    def get_all_persons(self) -> list[dict]:
        persons = self.session.query(Person).all()
        return [self._to_dict(p) for p in persons]

    def get_person_by_id(self, person_id: int) -> dict:
        person = self.session.query(Person).filter(Person.person_id == person_id).first()
        return self._to_dict(person) if person else None

    def update_person(self, person_id: int, name: str, surname: str) -> dict:
        person = self.session.query(Person).filter(Person.person_id == person_id).first()
        if person:
            person.name = name
            person.surname = surname
            return self._to_dict(person)
        return None

    def delete_person(self, person_id: int) -> bool:
        person = self.session.query(Person).filter(Person.person_id == person_id).first()
        if person:
            self.session.delete(person)
            return True
        return False

    def _to_dict(self, person: Person) -> dict:
        return {
            'person_id': person.person_id,
            'name': person.name,
            'surname': person.surname
        }