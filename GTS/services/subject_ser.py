from db.connection import DatabaseConnection
from repository.subject_rep import SubjectRepository

class SubjectService:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def create_subject(self, name: str) -> dict:
        with self.db_connection.get_session() as session:
            repository = SubjectRepository(session)
            return repository.create_subject(name)

    def get_all_subjects(self) -> list[dict]:
        with self.db_connection.get_session() as session:
            repository = SubjectRepository(session)
            return repository.get_all_subjects()

    def get_subject_by_id(self, subject_id: int) -> dict:
        with self.db_connection.get_session() as session:
            repository = SubjectRepository(session)
            return repository.get_subject_by_id(subject_id)

    def update_subject(self, subject_id: int, name: str) -> dict:
        with self.db_connection.get_session() as session:
            repository = SubjectRepository(session)
            return repository.update_subject(subject_id, name)

    def delete_subject(self, subject_id: int) -> bool:
        with self.db_connection.get_session() as session:
            repository = SubjectRepository(session)
            return repository.delete_subject(subject_id)