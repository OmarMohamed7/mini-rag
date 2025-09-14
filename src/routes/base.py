from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_settings, Config

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/")
async def home(app_settings: Config = Depends(get_settings)):
    appName = app_settings.APP_NAME
    appVersion = app_settings.APP_VERSION
    return {"message": f"Hello, {appName}! Version: {appVersion}"}
