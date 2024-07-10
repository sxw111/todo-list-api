from fastapi import FastAPI

from app.api.endpoints import api_router


app = FastAPI()

app.include_router(api_router)


@app.get("/")
async def root():
    return {"server is running": "OK"}
