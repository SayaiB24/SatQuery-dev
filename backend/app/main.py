from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.api.routes_analyze import router as analyze_router
from backend.app.api.routes_session import router as session_router
from backend.app.api.routes_system import router as system_router
from backend.app.config import (
    APP_DESCRIPTION,
    APP_TITLE,
    APP_VERSION,
    CORS_ORIGINS,
    STORAGE_DIR,
)

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local storage directory to serve image previews and reports
app.mount("/storage", StaticFiles(directory=str(STORAGE_DIR)), name="storage")

# Include API route modules
app.include_router(analyze_router)
app.include_router(session_router)
app.include_router(system_router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to SatQuery AI Backend API",
        "docs": "/docs",
        "health": "/v1/health",
        "registry": "/v1/registry",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
