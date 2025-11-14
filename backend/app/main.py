# backend/app/main.py
from fastapi import FastAPI
from app.api.v1.cv_routes import router as cv_router

app = FastAPI(
    title="CV Builder API",
    version="1.0.0",
    description="Backend service for CV generation and job parsing."
)

app.include_router(cv_router, prefix="/api/v1/cv", tags=["CV Builder"])

@app.get("/")
async def root():
    return {"message": "Welcome to the CV Builder API"}
