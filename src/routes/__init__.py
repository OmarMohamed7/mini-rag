from fastapi import FastAPI,APIRouter
import os

app_name = os.getenv("APP_NAME")
app_version = os.getenv("APP_VERSION")

router = APIRouter(
    prefix="/api/v1",
)

@router.get("/")
def read_root():
    return {"message": f"Hello, {app_name}! Version: {app_version}"}

