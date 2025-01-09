from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import pyodbc

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            load_dotenv()
            connection_string = os.getenv("DATABASE_URL")
            
            if not connection_string:
                raise ValueError("DATABASE_URL not found in environment variables")
            
            cls._instance.engine = create_engine(
                connection_string,
                fast_executemany=True,
                pool_pre_ping=True,
                
            )

            @event.listens_for(cls._instance.engine, 'connect')
            def set_isolation_level(dbapi_connection, connection_record):
                dbapi_connection.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
                dbapi_connection.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
                dbapi_connection.setencoding(encoding='utf-8')
            
            cls._instance.SessionLocal = sessionmaker(
                bind=cls._instance.engine,
                autocommit=False,
                autoflush=False
            )
            
        return cls._instance

    @contextmanager
    def get_session(self):
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()