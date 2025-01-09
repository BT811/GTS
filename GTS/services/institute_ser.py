from db.connection import DatabaseConnection
from repository.institute_rep import InstituteRepository

class InstituteService:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_institute(self, name: str, university_id: int) -> dict:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.create_institute(name, university_id)

    def get_all_institutes(self) -> list[dict]:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.get_all_institutes()

    def get_institute_by_id(self, institute_id: int) -> dict:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.get_institute_by_id(institute_id)

    def update_institute(self, institute_id: int, name: str, university_id: int) -> dict:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.update_institute(institute_id, name, university_id)

    def delete_institute(self, institute_id: int) -> bool:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.delete_institute(institute_id)

    def get_institutes_by_university(self, university_id: int) -> list[dict]:
        with self.db_connection.get_session() as session:
            repository = InstituteRepository(session)
            return repository.get_institutes_by_university(university_id)