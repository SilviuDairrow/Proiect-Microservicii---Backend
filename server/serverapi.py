#venv\Scripts\activate
#uvicorn serverapi:app --host 0.0.0.0 --port 8000 --reload
import asyncio
from datetime import datetime

import os

from typing import Union, List, Optional

import requests

from urllib.parse import quote

from pydantic import BaseModel
from pydantic import ValidationError

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi import File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from pymongo import MongoClient
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

from CRUD import create_disciplina, create_profesor, create_student
from CRUD import get_disciplina, get_profesor, get_student
from CRUD import update_disciplina, update_profesor, update_student
from CRUD import delete_disciplina, delete_profesor, delete_student

from Mongo_DB import create_resursa, get_resursa_by_COD, update_resursa

from schemas import JoinDSCreate
from schemas import ProfesorCreate, ProfesorResponse
from schemas import StudentCreate, StudentResponse
from schemas import DisciplinaCreate, DisciplinaResponse
from schemas import FileUploadResponse, FileMetadataResponse

from models import Student, Disciplina, JoinDS
from models import Base, Role, Mapa_Role
from models import CreereCont

import grpc
import auth_pb2
import auth_pb2_grpc
from auth_client import AuthClient

from pydantic import EmailStr

app = FastAPI()
auth_client = AuthClient()


DATABASE_URL = "mysql+mysqlconnector://root:mysql@db/mysql"
engine = create_engine(DATABASE_URL, echo=True)


MONGO_HOST = os.getenv("MONGO_HOST", "mongo")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_USERNAME = os.getenv("MONGO_INITDB_ROOT_USERNAME", "root")
MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "admin")
MONGO_DB = os.getenv("MONGO_DB", "materiale_db")
#mongodb_url = "mongodb://root:admin@mongo:27017"

#SEAWEEDFS_MASTER_URL = "http://192.168.56.1:9333"
#SEAWEEDFS_URL = "http://192.168.56.1:8083/"
SEAWEEDFS_MASTER_URL = "http://master:9333/"
SEAWEEDFS_URL = "http://volume:8083/"

mongo_client = MongoClient(
    f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
)

mongo_db = mongo_client[MONGO_DB]

materiale_collection = mongo_db["materiale"]
#TODO: implementat HATEOAS

app.mount("/static", StaticFiles(directory="html/static"), name="static")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("./html/default.html") as f:
        return HTMLResponse(content=f.read())


@app.post("/api/profesor", response_model=ProfesorResponse, status_code=201, response_description="Created. Create Profesor o mers cum trb")
def api_create_profesor(profesor: ProfesorCreate, db: Session = Depends(get_db)):
    try:
        create_profesor(db, profesor)
        #raise HTTPException(status_code=201, detail="Created. Create Profesor o mers cum trb")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Create Profesor nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Create Profesor nu o mers pt ca nu sunt detaliile corecte")
        
@app.post("/api/student", response_model=StudentResponse, status_code=201, response_description="Created. Create Student o mers cum trb")
def api_create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        create_student(db, student)
        #raise HTTPException(status_code=201, detail="Created. Create Student o mers cum trb")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Create Student nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Create Student nu o mers pt ca nu sunt detaliile corecte")      

@app.post("/api/disciplina", response_model=DisciplinaResponse, status_code=201, response_description="Created. Create Disciplina o mers cum trb")
def api_create_disciplina(disciplina: DisciplinaCreate, db: Session = Depends(get_db)):
    try:
        create_disciplina(db, disciplina)
        #raise HTTPException(status_code=201, response_description="Created. Create Disciplina o mers cum trb")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Create Disciplina nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Create Disciplina nu o mers pt ca nu sunt detaliile corecte")



@app.get("/api/profesor/{id}", response_model=ProfesorResponse, status_code=200, response_description="OK. Get Profesor o mers cum trb")
def api_get_profesor(id: int, db: Session = Depends(get_db)):
    try:
        #raise HTTPException(status_code=200, detail="OK. Get Profesor o mers cum trb")
        return get_profesor(db, id)
    except:
        raise HTTPException(status_code=404, detail="Not Found. Profesoru nu a fost gasit")

@app.get("/api/student/{id}", response_model=StudentResponse, status_code=200, response_description="OK. Get Student o mers cum trb")
def api_get_student(id: int, db: Session = Depends(get_db)):
    try:
        return get_student(db, id)
    except:
        raise HTTPException(status_code=404, detail="Not Found. Studentu nu a fost gasit")

@app.get("/api/disciplina/{COD}", response_model=DisciplinaResponse, status_code=200, response_description="OK. Get Disciplina o mers cum trb")
def api_get_disciplina(COD: str, db: Session = Depends(get_db)):
    try:
        return get_disciplina(db, COD)
    except:
        raise HTTPException(status_code=404, detail="Not Found. Disciplina nu a fost gasita")



@app.put("/api/profesor/update/{id}", response_model=ProfesorResponse, status_code=201, response_description="Created. Update Profesor o mers cum trb")
def api_update_profesor(id: int, profesor: ProfesorCreate, db: Session = Depends(get_db)):
    try:
        update_profesor(db, profesor)
        #raise HTTPException(status_code=201, response_description="Created. Update Profesor o mers cum trb")
    #aici mai e un 204 da nu inteleg care e contextul exact
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Update Profesor nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Update Profesor nu o mers pt ca nu sunt detaliile corecte")      
    
@app.put("/api/student/update/{id}", response_model=StudentResponse, status_code=201, response_description="Created. Update Student o mers cum trb")
def api_update_student(id: int, student = StudentCreate, db: Session = Depends(get_db)):
    try:
        update_student(db, student)
        #raise HTTPException(status_code=201, detail="Created. Update Student o mers cum trb")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Update Student nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Update Student nu o mers pt ca nu sunt detaliile corecte")      

@app.put("/api/disciplina/update/{COD}", response_model=DisciplinaResponse, status_code=201, response_description="Created. Update Disciplina o mers cum trb")
def api_update_disciplina(COD: int, disciplina = DisciplinaCreate, db: Session = Depends(get_db)):
    try:
        update_disciplina(db, disciplina)
        #raise HTTPException(status_code=201, detail="Created. Create Disciplina o mers cum trb")
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Conflict. Create Disciplina nu o mers pt ca exista deja profu")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="Unprocessable Content. Create Disciplina nu o mers pt ca nu sunt detaliile corecte")



@app.post("/api/profesor/delete/{id}", response_model=ProfesorResponse)
def api_delete_profesor(id: int, db: Session = Depends(get_db)):

    if delete_profesor(db, id):
        raise HTMLResponse(status_code=204, detail="Profesorul cu id: {id} a fost stars cu succes")
    else: 
        #200 si 202 nu au sens in contextu asta pt ca se sterge instant resursa la mn
        raise HTMLResponse(status_code=404, detail="Profesorul nu exista ca sa poata fi sters man")
    
@app.post("/api/student/delete/{id}", response_model=StudentResponse)
def api_delete_student(id: int, db: Session = Depends(get_db)):

    if delete_student(db, id):
        raise HTMLResponse(status_code=204, detail="Studentu cu id: {id} a fost stars cu succes")
    else: 
        raise HTMLResponse(status_code=404, detail="Studentu nu exista ca sa poata fi sters man")
    
@app.post("/api/disciplina/delete/{COD}", response_model=DisciplinaResponse)
def api_delete_disciplina(COD: int, db: Session = Depends(get_db)):

    if delete_disciplina(db, COD):
        raise HTMLResponse(status_code=204, detail="Disciplina cu id: {COD} a fost stars cu succes")
    else: 
        raise HTMLResponse(status_code=404, detail="Disciplina nu exista ca sa poata fi sters man")



@app.post("/api/student/{ID}/disciplina", status_code=201, response_model=JoinDSCreate, response_description="Enrolled. Studentul a fost inrolat cu succes la disciplina")
def api_student_enroll(ID: int, JOIN_DS: JoinDSCreate, db: Session = Depends(get_db)):

    student = db.query(Student).filter(Student.ID == ID).first()

    if not student:
        raise HTTPException(status_code=404, detail="Studentul nu exista.")
    
    disciplina = db.query(Disciplina).filter(Disciplina.COD == JOIN_DS.DisciplinaID).first()

    if not disciplina:
        raise HTTPException(status_code=404, detail="Disciplina nu exista.")
    
    verif_enroll = db.query(JoinDS).filter(
        JoinDS.StudentID == ID,
        JoinDS.DisciplinaID == JOIN_DS.DisciplinaID       
    ).first()

    if verif_enroll:
        raise HTTPException(status_code=409, detail="Studentul e deja inrolat la aceasta disciplina.")

    try:
        enroll = JoinDS(DisciplinaID=JOIN_DS.DisciplinaID, StudentID=ID)
        db.add(enroll)
        db.commit()

    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=500, detail="Eroare pe server la inrolarea unui student la disciplina.")
    

    return enroll        



@app.post("/api/disciplina/{COD}/upload", status_code=201, response_description="PDF uploadat cu succes!")
async def api_upload_files(COD: str, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):

    file_ids = []
    responses = []

    disciplina = db.query(Disciplina).filter(Disciplina.COD == COD).first()
    if not disciplina:
        raise HTTPException(status_code=404, detail=f"Disciplina cu COD {COD} nu exista in baza de date.")

    for file in files:
        file_ext = file.filename.split(".")[-1].lower()

        if file_ext != "pdf":
            raise HTTPException(status_code=415, detail="Unsupported Media Type. Doar pdf-uri man")

        file_content = file.file.read(1024)
        file_magic_nr = file_content[:4]

        if file_magic_nr != b"%PDF":
            raise HTTPException(status_code=409, detail="Conflict. Nu respecta continutul unui pdf normal")

        await file.seek(0)

        rasp = requests.get(f"{SEAWEEDFS_MASTER_URL}/dir/assign")
        if rasp.status_code != 200:
            raise HTTPException(status_code=500, detail="Eroare la obtinerea FID de la SeaweedFS Master.")
        
        data = rasp.json()
        fid = data.get("fid")
        publicUrl = data.get("publicUrl")
        # publicUrl = "192.168.56.1:8083"

        if not fid or not publicUrl:
            raise HTTPException(status_code=500, detail="Eroare la generarea FID sau obtinerea publicUrl.")

        form = {"file": (file.filename, file.file, file.content_type)}
        upload_response = requests.post(f"http://{publicUrl}/{fid}", files=form)
        print("fid = ", fid)

        if upload_response.status_code != 201:
            raise HTTPException(status_code=500, detail="Eroare la upload-ul fisierului in SeaweedFS.")
        
        try:
            materiale_collection.insert_one({
                "disciplina_cod": COD,
                "file_id": fid,
                "filename": file.filename,
                "content_type": file.content_type,
                "data_upload": datetime.now().isoformat(),
            })

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Eroare la inserare in MongoDB: {str(e)}")

        
        file_ids.append(fid)
        responses.append(
            {
                "message": "File Upload OK!",
                "file_id": fid,
                "filename": file.filename,
                "disciplina_cod": COD
            }
        )

    return JSONResponse(
        content={
            "message": "File Uploadate OK!",
            "files": responses
        },
        status_code=201
    )

@app.get("/api/disciplina/{COD}/file/{fid}", status_code=200, response_description="PDF downloadat cu succes")
async def api_get_file(COD: str, fid: str):

    file_metadata = materiale_collection.find_one({"file_id": fid, "disciplina_cod": COD})

    if not file_metadata:
        raise HTTPException(status_code=404, detail="PDF-ul nu mai exista")

    url_fila = f"{SEAWEEDFS_URL}/{quote(fid)}"

    try:
        rasp = requests.get(url_fila, stream=True)
        rasp.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Eroare pe server la preluat PDF-ul")
    
    temp_fila_path = f"./{fid}_{file_metadata['filename']}"

    with open(temp_fila_path, "wb") as temp_file:
        for bucata in rasp.iter_content(chunk_size=8192):
            temp_file.write(bucata)
    
    #print("path: " + temp_fila_path)

    if not os.path.exists(temp_fila_path):
        raise HTTPException(status_code=500, detail="Eroare la server. Nu s-a salvat fila temp pe server")

    #try:
    return FileResponse(temp_fila_path, 
                            media_type=f"f{file_metadata['content_type']}; charset=utf-8", 
                            filename=file_metadata['filename'],
                            headers={"Content-Disposition": f"attachment"})
    # except Exception as e:
    #     print("Eroare: " + str(e))
    #     print("metadata: " + file_metadata['content_type'])
    #     print("filename:" + file_metadata['filename'])
    #     raise HTTPException(status_code=500, detail="Eroare la preluat PDF-ul temp din server")
    # finally:
    #     if os.path.exists(temp_file_path):
    #         os.remove(temp_file_path)

@app.post("/api/disciplina/{COD}/file/{fid}", status_code=201, response_description="PDF sters cu succes")
async def api_delete_file(COD: str, fid: str):

    file_metadata = materiale_collection.find_one({"file_id": fid, "disciplina_cod": COD})

    if not file_metadata:
        raise HTTPException(status_code=404, response_description="PDF-ul nu mai exista")
    
    url_fila = f"{SEAWEEDFS_URL}/{quote(fid)}"

    try:
        rasp = requests.delete(url_fila)
        materiale_collection.delete_one({"file_id": fid, "disciplina_cod": COD})

        rasp.raise_for_status()

    except requests.RequestException as eroare:
        # print(f"Error deleting the file: {eroare}")
        # print(f"Response status code: {response.status_code}")
        # print(f"Response content: {response.text}")
        raise HTTPException(status_code=500, detail="Eroare pe server la stergerea PDF-ului man")

@app.put("/api/disciplina/{COD}/file/{fid}", status_code=201, response_description="PDF modificat/inlocuit cu succes")
async def api_update_file(COD: str, fid: str, file: UploadFile = File(...), db: Session = Depends(get_db)):

    file_metadata = materiale_collection.find_one({"file_id": fid, "disciplina_cod": COD})
    
    if not file_metadata:
        raise HTTPException(status_code=404, detail="PDF-ul nu mai exista in baza de date")

    url_fila = f"{SEAWEEDFS_URL}/{quote(fid)}"
    try:
        rasp = requests.delete(url_fila)
        rasp.raise_for_status()
    except requests.RequestException as e:
        print(f"Eroare la stergerea PDF-ului din Seaweed: {e}")
        raise HTTPException(status_code=500, detail="Eroare la stergerea PDF-ului din SeaweedFS")

    file_ext = file.filename.split(".")[-1].lower()

    if file_ext != "pdf":
        raise HTTPException(status_code=415, detail="Unsupported Media Type. Doar pdf-uri man")

    file_content = file.file.read(1024)
    file_magic_nr = file_content[:4]

    if file_magic_nr != b"%PDF":
        raise HTTPException(status_code=409, detail="Conflict. Nu respecta continutul unui pdf normal")

    await file.seek(0)

    rasp = requests.get(f"{SEAWEEDFS_MASTER_URL}/dir/assign")
    if rasp.status_code != 200:
        raise HTTPException(status_code=500, detail="Eroare la obtinerea FID de la SeaweedFS Master.")
    
    data = rasp.json()
    new_fid = data.get("fid")
    publicUrl = data.get("publicUrl")

    if not new_fid or not publicUrl:
        raise HTTPException(status_code=500, detail="Eroare la generarea FID sau obtinerea publicUrl.")

    form = {"file": (file.filename, file.file, file.content_type)}
    upload_url = f"http://{publicUrl}/{new_fid}"
    upload_response = requests.post(upload_url, files=form)

    if upload_response.status_code != 201:
        raise HTTPException(status_code=500, detail="Eroare la upload-ul fisierului in SeaweedFS.")
    
    try:
        materiale_collection.update_one(
            {"file_id": fid, "disciplina_cod": COD},
            {
                "$set": {
                    "file_id": new_fid,
                    "filename": file.filename,
                    "content_type": file.content_type,
                    "data_upload": datetime.now().isoformat(),
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare la actualizarea in MongoDB: {str(e)}")

    return JSONResponse(
        content={
            "message": "PDF actualizat cu succes!",
            "file_id": new_fid,
            "filename": file.filename,
            "disciplina_cod": COD
        },
        status_code=201
    )



@app.on_event("shutdown")
def shutdown_server():

    auth_client.close()



@app.post("/auth/verif-sesiune", status_code=201, response_description="S-a verificat sesiunea")
async def VerifSesiune(refresh_token: str):

    try:
        rasp = await asyncio.to_thread(auth_client.verif_sesiune, refresh_token)
        return {"email": rasp.email, "role": rasp.role}
    
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"Eroare la verificarea sesiunii: {str(e)}")
    
@app.post("/auth/login", status_code=201, response_description="Ai fost logat cu succes")
async def login(email: EmailStr, password: str):

    try:
        #parola_criptata = auth_client.criptare_parola(password)

        rasp = await asyncio.to_thread(auth_client.login, email, password)

        return {"refresh_token": rasp.refresh_token}

    except grpc.RpcError as e:
        if e.code() == grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(status_code=401, detail="E-mail sau parola incorecte.")
        else:
            raise HTTPException(status_code=500, detail=f"Eroare la login: {str(e)}")            

@app.post("/auth/creere-cont", status_code=201, response_description="Contul a fost creeat cu succes")
async def creereCont(email: EmailStr, password: str, role: str):
    try:
        parola_criptata = auth_client.criptare_parola(password)
        
        role_int = Mapa_Role[role]

        rasp = await asyncio.to_thread(
            auth_client.creeare_cont,
            email,
            parola_criptata,
            role_int
        )
        
        return {"message": "Contul a fost creat cu succes."}

    except grpc.RpcError as eroare:
        if eroare.code() == grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(status_code=409, detail="Exista deja un cont cu aceste date.")
        else:
            raise HTTPException(status_code=500, detail=f"Eroare pe svr la crearea contului: {str(eroare)}")



# TODO:
# Login cu gRPC (X)
# Creere client in fastapiu meu ca sa pot accesa loginul (~IN PROGRESS~)
# JWT cu refresh token si access token
# Ruta Update file (X)
# Ruta Delete file (X)