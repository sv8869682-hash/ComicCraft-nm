from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import settings, STATIC_DIR
from app.routes import router

app = FastAPI(title=settings.app_name, version="1.0.0", description="AI Comic Story Creator using Gemini and image generation")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "image_provider": settings.image_provider}
