from enum import Enum
from pydantic import BaseModel, field_validator, validator
from typing import List, Optional
from bson import ObjectId

class ProfesorCreate(BaseModel):
    nume: str
    prenume: str
    email: str

    grad_didactic: Optional[str]

    tip_asociere: str

    afiliere: Optional[str]

class DisciplinaCreate(BaseModel):
    COD: str

    ID_titular: int

    nume_disciplina: str

    an_studiu: int

    tip_disciplina: str

    categorie_disciplina: str
    tip_examinare: str

class StudentCreate(BaseModel):
    nume: str
    prenume: str
    email: str

    ciclu_studii: str

    an_studiu: int
    grupa: int

class JoinDSCreate(BaseModel):
    DisciplinaID: str
    StudentID: int

class ProfesorResponse(BaseModel):
    ID: int

    nume: str
    prenume: str
    email: str

    grad_didactic: Optional[str]

    tip_asociere: str

    afiliere: Optional[str]

    class Config:
        from_attribute = True

class DisciplinaResponse(BaseModel):
    COD: str

    ID_titular: int

    nume_disciplina: str

    an_studiu: int

    tip_disciplina: str

    categorie_disciplina: str

    tip_examinare: str

    class Config:
        from_attribute = True

class StudentResponse(BaseModel):
    ID: int

    nume: str
    prenume: str
    email: str

    ciclu_studii: str
    
    an_studiu: int
    grupa: int

    class Config:
        from_attributes = True

class JoinDSCreate(BaseModel):
    DisciplinaID: str
    #StudentID: int

    class Config:
        from_attribute = True

class FileUploadResponse(BaseModel):
    message: str
    file_id: str
    filename: str
    disciplina_cod: int

class FileMetadataResponse(BaseModel):
    file_id: str
    filename: str
    content_type: str
    message: Optional[str] = "FIla primita cu succes"

    class Config:
        orm_mode = True


############ MONGODB ############

class GradeWeight(BaseModel):
    id: Optional[str] 
    name: str
    weight: float


class File(BaseModel):
    id: Optional[str]
    seaweed_fid: str
    name: str
    mime_type: str


class Resource(BaseModel):
    id: Optional[str]
    lecture_code: str
    grades: List[GradeWeight]
    files: List[File]