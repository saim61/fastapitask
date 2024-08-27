from fastapi.middleware.cors import CORSMiddleware as cors

from routes.candidate_routes import router as candidate_router, router_two as candidate_router_two
from routes.user_routes import router as user_router
from routes.home_routes import home_router
from auth.auth import router as auth_router

from dotenv import load_dotenv
from fastapi import FastAPI

import sentry_sdk
import os
import uvicorn

from utils.utils import APP_TITLE, APP_DESCRIPTION

load_dotenv()
SENTRY_DSN: str = os.getenv("SENTRY_DSN")

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION
)

app.add_middleware(
    cors,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

app.include_router(candidate_router)
app.include_router(candidate_router_two)
app.include_router(user_router)
app.include_router(home_router)
app.include_router(auth_router)

if __name__ == '__main__':
    print("Starting your server.")
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)