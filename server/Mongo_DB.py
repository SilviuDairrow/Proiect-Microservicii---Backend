from datetime import datetime
from bson import ObjectId
from typing import List, Optional
from pymongo.collection import Collection

def create_resursa(materiale_collection: Collection, disciplina_COD: str, grades: List[dict], files: List[dict]) -> dict:

    resursa_data = {
        "disciplina_COD": disciplina_COD,
        "grades": grades,
        "files": files,
        "created_at": datetime.utcnow(),
    }

    rezultat = materiale_collection.insert_one(resursa_data)
    return {"id": str(rezultat.inserted_id), **resursa_data}

def get_resursa_by_COD(materiale_collection: Collection, disciplina_COD: str) -> dict:

    resursa = materiale_collection.find_one({"disciplina_COD": disciplina_COD})

    if resursa:
        resursa["_id"] = str(resursa["_id"])  
        return resursa
    return None

def update_resursa(materiale_collection: Collection, resursa_id: str, grades: Optional[List[dict]] = None, files: Optional[List[dict]] = None) -> dict:
    
    resursa_id = ObjectId(resursa_id)
    
    update_data = {}
    if grades:
        update_data["grades"] = grades
    if files:
        update_data["files"] = files

    rezultat = materiale_collection.update_one(
        {"_id": resursa_id},
        {"$set": update_data}
    )

    if rezultat.modified_count > 0:
        return {"message": "O mers update la resurse."}
    else:
        return {"message": "Eroare la introducere metadate in DB."}
