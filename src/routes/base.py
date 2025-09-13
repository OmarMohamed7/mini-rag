from fastapi import FastAPI,APIRouter
from helpers.config import get_settings

router = APIRouter(
    prefix="/api/v1",
)

@router.get("/")
async def read_root():
    app_settings = get_settings()
    appName = app_settings.APP_NAME
    appVersion = app_settings.APP_VERSION
    return {"message": f"Hello, {appName}! Version: {appVersion}"}

