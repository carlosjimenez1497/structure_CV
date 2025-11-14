# backend/app/main.py
from fastapi import FastAPI

from app.api.v1.cv_routes import router as cv_router
from app.api.v1.auth_routes import router as auth_router
from app.api.v1.profile_routes import router as profile_router

app = FastAPI(
    title="CV Builder API",
    version="1.0.0",
    description="Backend service for CV generation and job parsing."
)

@app.get("/")
async def root():
    return {"message": "Welcome to the CV Builder API"}

# Routers
app.include_router(auth_router,    prefix="/api/v1/auth",    tags=["Auth"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["Profile"])
app.include_router(cv_router,      prefix="/api/v1/cv",      tags=["CV Builder"])
