from fastapi import FastAPI

app = FastAPI(
    title="StudyAI API",
    description="Backend para o App StudyAI",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "API seguindo corretamente fluxo Nginx -> Kong -> API"}
