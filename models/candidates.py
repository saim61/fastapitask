from bson import ObjectId
from pydantic import BaseModel

from config.database import candidates_collection_name

class Candidate(BaseModel):
    id: str
    gender: str
    name: str
    phone: str

class CandidateRequest(BaseModel):
    gender: str
    name: str
    phone: str

def candidate_serializer(candidate: Candidate) -> dict:
    return {
        "id": str(candidate["_id"]),
        "name": candidate["name"],
        "gender": candidate["gender"],
        "phone": candidate["phone"]
    }

def candidates_serialize(candidates) -> list:
    return [candidate_serializer(candidate) for candidate in candidates]

def find_candidate_by_id(_id: str) -> dict:
    the_candidate = candidates_collection_name.find_one({"_id": ObjectId(_id)})
    if the_candidate is None:
        return {}

    return candidate_serializer(the_candidate)

def get_all_candidates() -> list[Candidate]:
    return candidates_serialize(candidates_collection_name.find())

def insert_candidate(candidate: CandidateRequest):
    return candidates_collection_name.insert_one(dict(candidate))

def update_candidate(_id: str, candidate: CandidateRequest):
    return candidates_collection_name.find_one_and_update({"_id": ObjectId(_id)}, {"$set": dict(candidate)})

def delete_candidate(_id: str):
    return candidates_collection_name.find_one_and_delete({"_id": ObjectId(_id)})

def delete_all_candidates():
    candidates_collection_name.drop()