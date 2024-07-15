from fastapi import FastAPI

from app.api.endpoints import api_router
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.TITLE,
    version=settings.VERSION,
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.IS_ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
