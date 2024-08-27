from http.client import HTTPException
from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends

from auth.auth import oauth2_bearer
from starlette import status
from models.candidates import Candidate, CandidateRequest, find_candidate_by_id, get_all_candidates, insert_candidate, update_candidate, delete_candidate
from utils.utils import CANDIDATE_ADDED, CANDIDATE_NOT_FOUND, CANDIDATE_ADDED_ERROR, CANDIDATE_UPDATED, \
    CANDIDATE_UPDATED_ERROR, CANDIDATE_DELETED, CANDIDATE_DELETED_ERROR

router = APIRouter(
    prefix="/candidate",
    tags=["candidate"]
)

router_two = APIRouter(
    prefix="/all-candidates",
    tags=["candidate"]
)

# GET get candidate endpoint
@router.get("/{_id}")
async def get_candidate(_id: str, token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Get candidate information

    Args:
        _id (str): ID of candidate.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself

    Raises:
        HTTPException: 404 Not Found if candidate doesn't exist in DB.

    Returns:
        Response: 200 OK with candidate details.
    """
    candidate = find_candidate_by_id(_id)
    if bool(candidate):
        return candidate
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=CANDIDATE_NOT_FOUND)
    
# POST add candidate endpoint
@router.post("/")
async def add_candidate(candidate: CandidateRequest, token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Add a new candidate.

    Args:
        candidate (CandidateRequest): Candidate information.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself.

    Raises:
        HTTPException: 400 Bad Request if some error occurred while adding candidate.

    Returns:
        Response: 200 OK with message that Candidate was added.
    """
    if insert_candidate(candidate):
        raise HTTPException(status_code=status.HTTP_200_OK, detail=CANDIDATE_ADDED)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=CANDIDATE_ADDED_ERROR)

# PUT update candidate endpoint
@router.put("/{_id}")
async def update(_id: str, candidate: CandidateRequest, token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Update candidate information.

    Args:

        _id (str): ID of candidate.
        candidate (CandidateRequest): Candidate information to be updated.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself

    Raises:
        HTTPException: 400 Bad Request if some error occurred while updating candidate.

    Returns:
        Response: 200 OK with message that Candidate was updated.
    """
    if update_candidate(_id, candidate):
        raise HTTPException(status_code=status.HTTP_200_OK, detail=CANDIDATE_UPDATED)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=CANDIDATE_UPDATED_ERROR)

# DELETE delete candidate endpoint
@router.delete("/{_id}")
async def delete(_id: str, token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Delete a candidate.

    Args:
        _id (str): ID of candidate.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself

    Raises:
        HTTPException: 400 Bad Request if some error occurred while deleting candidate.

    Returns:
        Response: 200 OK with message that Candidate was deleted.
    """
    if delete_candidate(_id):
        raise HTTPException(status_code=status.HTTP_200_OK, detail=CANDIDATE_DELETED)
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=CANDIDATE_DELETED_ERROR)

# GET all candidates endpoint
@router_two.get("")
async def all_candidate(token: Annotated[str, Depends(oauth2_bearer)]) -> list[Candidate]:
    """
    Get all candidate information.

    Args:
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself

    Returns:
        Response: 200 OK with list of all Candidates.
    """
    return get_all_candidates()