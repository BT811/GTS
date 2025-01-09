from dataclasses import dataclass
from enum import Enum
from datetime import date
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum as SQLAEnum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ThesisType(str, Enum):
    Master = "Master"
    Doctorate = "Doctorate"
    SPECIALIZATION_IN_MEDICINE = "Specialization in Medicine"
    PROFICIENCY_IN_ART = "Proficiency in Art"

class Language(str, Enum):
    TURKISH = "Turkish"
    ENGLISH = "English"


@dataclass
class University:
    university_id: int
    name: str
    institutes: List['Institute'] = None

class University(Base):
    __tablename__ = 'UNIVERSITY'
    
    university_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

@dataclass
class Institute:
    institute_id: int
    university_id: int
    name: str
    university: Optional[University] = None

class Institute(Base):
    __tablename__ = 'INSTITUTE'
    
    institute_id = Column(Integer, primary_key=True)
    university_id = Column(Integer, ForeignKey('UNIVERSITY.university_id'), nullable=False)
    name = Column(String(50))

@dataclass
class Person:
    person_id: int
    name: str
    surname: str
    password: str

class Person(Base):
    __tablename__ = 'PERSON'
    
    person_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)

@dataclass
class CoSupervisorThesis:
    thesis_id: int
    person_id: int

class CoSupervisorThesis(Base):
    __tablename__ = 'CO_SUPERVISOR_THESIS'
    
    thesis_id = Column(Integer, ForeignKey('THESIS.thesis_id'), primary_key=True)
    person_id = Column(Integer, ForeignKey('PERSON.person_id'), primary_key=True)

@dataclass
class Keyword:
    keyword_id: int
    thesis_id: int
    name: str

class Keyword(Base):
    __tablename__ = 'KEYWORD'
    
    keyword_id = Column(Integer, primary_key=True)
    thesis_id = Column(Integer, ForeignKey('THESIS.thesis_id'))
    name = Column(String(255))

@dataclass
class ThesisSubject:
    thesis_id: int
    subject_id: int

class ThesisSubject(Base):
    __tablename__ = 'THESIS_SUBJECT'
    
    thesis_id = Column(Integer, ForeignKey('THESIS.thesis_id'), primary_key=True)
    subject_id = Column(Integer, ForeignKey('SUBJECT.subject_id'), primary_key=True)

@dataclass
class Thesis:
    thesis_id: int
    author_id: int
    supervisor_id: int
    title: str
    abstract: str
    year: int
    type: ThesisType
    university_id: int
    institute_id: int
    number_of_pages: int
    language: Language
    submission_date: date

    def __post_init__(self):
        if not isinstance(self.type, ThesisType):
            try:
                self.type = ThesisType(self.type)
            except ValueError:
                raise ValueError(f"Invalid thesis type. Must be one of {[t.value for t in ThesisType]}")
        
        if not isinstance(self.language, Language):
            try:
                self.language = Language(self.language)
            except ValueError:
                raise ValueError(f"Invalid language. Must be one of {[l.value for l in Language]}")

class Thesis(Base):
    __tablename__ = 'THESIS'
    
    thesis_id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('PERSON.person_id'), nullable=False)
    supervisor_id = Column(Integer, ForeignKey('PERSON.person_id'), nullable=False)
    title = Column(String(500), nullable=False)
    abstract = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(String(50), nullable=False)
    university_id = Column(Integer, ForeignKey('UNIVERSITY.university_id'))
    institute_id = Column(Integer, ForeignKey('INSTITUTE.institute_id'))
    number_of_pages = Column(Integer, nullable=False)
    language = Column(String(50), nullable=False)
    submission_date = Column(Date, nullable=False)

    @property
    def thesis_type(self):
        return ThesisType(self.type) if self.type else None

    @property
    def thesis_language(self):
        return Language(self.language) if self.language else None

class Subject(Base):
    __tablename__ = 'SUBJECT'
    
    subject_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
