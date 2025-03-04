from sqlalchemy.orm import Session
from models import Profesor, Disciplina, Student
from schemas import ProfesorCreate, DisciplinaCreate, StudentCreate
from pymongo.collection import Collection
from bson import ObjectId

def create_profesor(db: Session, profesor: ProfesorCreate):
    db_profesor = Profesor(**profesor.dict())
    db.add(db_profesor)
    db.commit()
    db.refresh(db_profesor)
    return db_profesor

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def create_disciplina(db: Session, disciplina: DisciplinaCreate):
    db_disciplina = Disciplina(**disciplina.model_dump())
    db.add(db_disciplina)
    db.commit()
    db.refresh(db_disciplina)
    return db_disciplina

def get_profesor(db: Session, profesor_id: int):
    return db.query(Profesor).filter(Profesor.ID == profesor_id).first()

def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.ID == student_id).first()

def get_disciplina(db: Session, disciplina_COD: str):
    return db.query(Disciplina).filter(Disciplina.COD == disciplina_COD).first()

def update_profesor(db: Session, profesor_id: int, profesor: ProfesorCreate):
    db_profesor = db.query(Profesor).filter(Profesor.ID == profesor_id).first()
    if db_profesor:
        for key, value in profesor.model_dump().items():
            setattr(db_profesor, key, value)
        db.commit()
        db.refresh(db_profesor)
        return db_profesor
    return None

def update_student(db: Session, student_id: int, student: StudentCreate):
    db_student = db.query(Student).filter(Student.ID == student_id).first()
    if db_student:
        for key, value in student.model_dump().items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        return db_student
    return None

def update_disciplina(db: Session, disciplina_id: int, disciplina: DisciplinaCreate):
    db_disciplina = db.query(Disciplina).filter(Disciplina.ID == disciplina_id).first()
    if db_disciplina:
        for key, value in disciplina.model_dump().items():
            setattr(db_disciplina, key, value)
        db.commit()
        db.refresh(db_disciplina)
        return db_disciplina
    return None


def delete_profesor(db: Session, profesor_id: int):
    db_profesor = db.query(Profesor).filter(Profesor.ID == profesor_id).first()
    if db_profesor:
        db.delete(db_profesor)
        db.commit()
        return True
    return False

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.ID == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False



def delete_disciplina(db: Session, disciplina_id: int):
    db_disciplina = db.query(Disciplina).filter(Disciplina.ID == disciplina_id).first()
    if db_disciplina:
        db.delete(db_disciplina)
        db.commit()
        return True
    return False






#Pentru MongoDB ig


# def create_materiale(db: Collection, materiale: MaterialeCreate):
#     materiale_noi = materiale.model_dump()

#     rezultat = db.insert_one(materiale_noi)
#     materiale_noi["_id"] = str(rezultat.inserted_id)

#     return materiale_noi

# def get_materiale(db: Collection, materiale_id: str):
#     materiale = db.find_one({"_id": ObjectId(materiale_id)})

#     if materiale:
#         materiale["_id"] = str(materiale["_id"])

#     return materiale

# def get_all_materiale(db: Collection):
#     materiale_list = list(db.find())

#     for materiale in materiale_list:
#         materiale["_id"] = str(materiale["_id"])

#     return materiale_list

# def delete_materiale(db: Collection, materiale_id: str):
#     result = db.delete_one({"_id": ObjectId(materiale_id)})
    
#     return result.deleted_count > 0