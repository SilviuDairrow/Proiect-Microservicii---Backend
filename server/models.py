from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from pydantic import EmailStr

Base = declarative_base()

class Profesor(Base):
    __tablename__ = 'PROFESORI'

    ID = Column(Integer, primary_key=True, index=True)

    nume = Column(String(40), nullable=False)
    prenume = Column(String(70), nullable=False)
    email = Column(String(140), unique=True, nullable=False)

    grad_didactic = Column(Enum('asist', 'sef_lucr', 'conf', 'prof'))
    tip_asociere = Column(Enum('titular', 'asociat', 'extern'), nullable=False)
    
    afiliere = Column(String(70))



class Disciplina(Base):
    __tablename__ = 'DISCIPLINE'

    COD = Column(String(10), primary_key=True)
    ID_titular = Column(Integer, ForeignKey('PROFESORI.ID'), nullable=False)

    nume_disciplina = Column(String(100), nullable=False)
    an_studiu = Column(Integer, nullable=False)
    tip_disciplina = Column(Enum('impusa', 'optionala', 'liber_aleasa'), nullable=False)

    categorie_disciplina = Column(Enum('domeniu', 'specialitate', 'adiacenta'), nullable=False)

    tip_examinare = Column(Enum('examen', 'colocviu'), nullable=False)

class Student(Base):
    __tablename__ = 'STUDENTI'

    ID = Column(Integer, primary_key=True, index=True)

    nume = Column(String(40), nullable=False)
    prenume = Column(String(70), nullable=False)
    email = Column(String(140), unique=True, nullable=False)

    ciclu_studii = Column(Enum('licenta', 'master'), nullable=False)
    an_studiu = Column(Integer, nullable=False)
    grupa = Column(Integer, nullable=False)

class JoinDS(Base):
    __tablename__ = 'JOIN_DS'

    DisciplinaID = Column(String(10), ForeignKey('DISCIPLINE.COD'), primary_key=True)
    StudentID = Column(Integer, ForeignKey('STUDENTI.ID'), primary_key=True)

##############################################

Mapa_Role = {
    "student": 0,
    "profesor": 1,
    "admin": 2
}

class Role(str, Enum):
    student = "student"
    profesor = "profesor"
    admin = "admin"

class VerifSesiune(BaseModel):
    refresh_token: str

class CreereCont(BaseModel):
    email: EmailStr
    password: str
    role: Role

    class Config:
        arbitrary_types_allowed = True

class CreereSesiune(BaseModel):
    email: EmailStr
    password: str
    