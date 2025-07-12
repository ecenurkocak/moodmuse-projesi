from fastapi import FastAPI

from backend.api import auth, analysis

app = FastAPI(title="MoodMuse API")

# Router'ları ana uygulamaya dahil et
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["Analysis"])


@app.get("/")
def read_root():
    return {"message": "Welcome to MoodMuse API"} 