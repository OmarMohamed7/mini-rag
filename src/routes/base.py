from fastapi import FastAPI, APIRouter, Depends
from helpers.config import get_config, Config

router = APIRouter(
    prefix="/api/v1",
)


@router.get("/")
async def home(app_settings: Config = Depends(get_config)):
    appName = app_settings.APP_NAME
    appVersion = app_settings.APP_VERSION
    return {"message": f"Hello, {appName}! Version: {appVersion}"}
