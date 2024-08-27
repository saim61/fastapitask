from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi.responses import StreamingResponse
from models.candidates import get_all_candidates
from models.users import get_all_users
from auth.auth import router, oauth2_bearer
from typing import Annotated
from io import BytesIO
from starlette import status

import pandas as pd

home_router = APIRouter()

# homepage
@home_router.get("/")
async def homepage():
    """
    Homepage route

    Returns:
        Response: 200 OK with a message saying Welcome to homepage.
    """
    raise HTTPException(status_code=status.HTTP_200_OK, detail="Welcome to homepage")

# GET generate report endpoint
@home_router.get("/generate-report")
async def generate_report(token: Annotated[str, Depends(oauth2_bearer)]):
    """
    Generate an Excel file with candidates and users in separate sheets

    Args:
        token (Annotated[str, Depends(oauth2_bearer)]): Your JWT token in headers once you authorize yourself

    Returns:
        Response: 200 OK with a file that can be downloaded via clicking on a link.
    """
    users_data = get_all_users()
    candidates_data = get_all_candidates()

    users_df = pd.DataFrame(users_data)
    candidates_df = pd.DataFrame(candidates_data)

    # Prepare Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        users_df.to_excel(writer, sheet_name='Users', index=False)
        candidates_df.to_excel(writer, sheet_name='Candidates', index=False)

    # Set up the response
    output.seek(0)
    response = StreamingResponse(output, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response.headers["Content-Disposition"] = "attachment; filename=report.xlsx"
    response.status_code=status.HTTP_200_OK
    response.body = {"detail": "Report generated and ready for download."}

    return response

# GET health end point
@home_router.get("/health")
async def healthcheck():
    """
   Health check route

   Returns:
       Response: 200 OK with a message saying API is healthy.
   """
    raise HTTPException(status_code=status.HTTP_200_OK, detail="API is healthy")