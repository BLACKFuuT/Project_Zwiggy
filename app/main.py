from fastapi import FastAPI
from .auth.router import router as auth_router

app = FastAPI(title="Smart Order Platform")

app.include_router(auth_router)
