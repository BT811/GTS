from db.connection import DatabaseConnection
from repository.person_rep import PersonRepository

class PersonService:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_person(self, name: str, surname: str, password: str) -> dict:
        with self.db_connection.get_session() as session:
            repository = PersonRepository(session)
            return repository.create_person(name, surname, password)

    def get_all_persons(self) -> list[dict]:
        with self.db_connection.get_session() as session:
            repository = PersonRepository(session)
            return repository.get_all_persons()

    def get_person_by_id(self, person_id: int) -> dict:
        with self.db_connection.get_session() as session:
            repository = PersonRepository(session)
            return repository.get_person_by_id(person_id)

    def update_person(self, person_id: int, name: str, surname: str) -> dict:
        with self.db_connection.get_session() as session:
            repository = PersonRepository(session)
            return repository.update_person(person_id, name, surname)

    def delete_person(self, person_id: int) -> bool:
        with self.db_connection.get_session() as session:
            repository = PersonRepository(session)
            return repository.delete_person(person_id)