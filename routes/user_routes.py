from http.client import HTTPException
from typing import Annotated

from fastapi import HTTPException, APIRouter, Depends

from auth.auth import bcrypt_context, oauth2_bearer
from starlette import status
from utils.utils import is_valid_username, INVALID_USERNAME, USER_EXISTS, USER_ADDED, USER_ADDED_ERROR, USER_NOT_FOUND, \
    SIGN_UP_SUCCESSFUL
from models.users import SignUpUserRequest, find_user_by_id, find_user_by_username, insert_user

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

# POST add users endpoint
@router.post("")
async def add_user(token: Annotated[str, Depends(oauth2_bearer)], user_data: SignUpUserRequest):
    """
    Add a new user.

    Args:
        user_data (SignUpUserRequest): User data.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself.

    Raises:
        HTTPException: 400 Bad Request if user already exists, an invalid username was provided or some error occurred while adding user.

    Returns:
        Response: 200 OK with a message indicating User added successfully.
    """
    user = find_user_by_username(username=user_data.username)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USER_EXISTS)
    
    if not is_valid_username(user_data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_USERNAME)
    
    username: str = user_data.username.lower()
    hashed_password: str = bcrypt_context.hash(user_data.password)
    user_data.username, user_data.password = username, hashed_password
    
    if insert_user(user_data):
        raise HTTPException(status_code=status.HTTP_200_OK, detail=USER_ADDED)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USER_ADDED_ERROR)

# GET get candidate endpoint
@router.get("/{_id}")
async def get_user(token: Annotated[str, Depends(oauth2_bearer)], _id: str):
    """
    Get details of a user.

    Args:
        _id (str): ID of user in DB.
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself.

    Raises:
        HTTPException: 400 Bad Request if user not found.

    Returns:
        Response: 200 OK with user details.
    """
    user = find_user_by_id(_id)
    if bool(user):
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)

# POST add candidate endpoint
@router.post("/sign_up")
async def sign_up(user: SignUpUserRequest):
    """
    Add a new user once you're signed in.

    Args:
        user (SignUpUserRequest): User data.

    Raises:
        HTTPException: 400 Bad Request if user already exists, an invalid username was provided.

    Returns:
        Response: 200 OK with a message indicating Sign up successful.
    """
    if find_user_by_username(user.username) != {}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=USER_EXISTS)

    if not is_valid_username(user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=INVALID_USERNAME)
    
    username: str = user.username.lower()
    hashed_password: str = bcrypt_context.hash(user.password)

    user.username, user.password = username, hashed_password

    insert_user(user)
    raise HTTPException(status_code=status.HTTP_200_OK, detail=SIGN_UP_SUCCESSFUL)