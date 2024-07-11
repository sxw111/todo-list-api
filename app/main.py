from fastapi import FastAPI

from app.api.endpoints import api_router


app = FastAPI()

app.include_router(api_router)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
