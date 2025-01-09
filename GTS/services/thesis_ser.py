from entities.entities import Thesis
from repository.thesis_rep import ThesisRepository
from db.connection import DatabaseConnection
from typing import Dict, Any

class ThesisService:
    def __init__(self):
        self.db_connection = DatabaseConnection()

    def get_thesis_by_id(self, thesis_id: int) -> Thesis:
        with self.db_connection.get_session() as session:
            repository = ThesisRepository(session)
            return repository.get_thesis_by_id(thesis_id)

    def search_theses(self, criteria: Dict[str, Any]) -> list[dict]:
        with self.db_connection.get_session() as session:
            repository = ThesisRepository(session)
            return repository.search_theses(criteria)

    def create_thesis(self, thesis_data: Dict[str, Any]) -> dict:
        self._validate_thesis_data(thesis_data)
        
        with self.db_connection.get_session() as session:
            repository = ThesisRepository(session)
            return repository.create_thesis(thesis_data)

    def _validate_thesis_data(self, thesis_data: Dict[str, Any]):
        author_id = thesis_data['author_id']
        supervisor_id = thesis_data['supervisor_id']
        co_supervisor_ids = thesis_data.get('co_supervisor_ids', [])

        required_fields = ['title', 'abstract', 'year', 'type', 'number_of_pages', 
                          'language', 'author_id', 'supervisor_id']
        for field in required_fields:
            if not thesis_data.get(field):
                raise ValueError(f"Missing required field: {field}")

        if author_id == supervisor_id:
            raise ValueError("Author cannot be the supervisor")
        
        if author_id in co_supervisor_ids:
            raise ValueError("Author cannot be a co-supervisor")
        
        if supervisor_id in co_supervisor_ids:
            raise ValueError("Supervisor cannot be a co-supervisor")
        
        if len(set(co_supervisor_ids)) != len(co_supervisor_ids):
            raise ValueError("Duplicate co-supervisors are not allowed")