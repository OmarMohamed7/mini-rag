from fastapi import FastAPI
import uvicorn
from routes import base

app = FastAPI()

app.include_router(base.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)