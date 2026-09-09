from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Resume Parser API", version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"success": True, "message": "Resume Parser API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
