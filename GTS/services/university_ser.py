from db.connection import DatabaseConnection
from repository.university_rep import UniversityRepository

class UniversityService:
    def __init__(self):
        self.db_connection = DatabaseConnection()
    
    def create_university(self, name: str):
        with self.db_connection.get_session() as session:
            repository = UniversityRepository(session)
            return repository.create_university(name)
    
    def get_all_universities(self):
        with self.db_connection.get_session() as session:
            repository = UniversityRepository(session)
            return repository.get_all_universities()
    
    def delete_university(self, university_id: int):
        with self.db_connection.get_session() as session:
            repository = UniversityRepository(session)
            return repository.delete_university(university_id)
    
    def update_university(self, university_id: int, name: str):
        with self.db_connection.get_session() as session:
            repository = UniversityRepository(session)
            return repository.update_university(university_id, name)
    
    def get_university_by_id(self, university_id: int):
        with self.db_connection.get_session() as session:
            repository = UniversityRepository(session)
            return repository.get_university_by_id(university_id)