from fastapi import HTTPException, status

from app.utilities.messages.exc_details import http_403_access_denied_details

async def http_403_exc_access_denied_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=http_403_access_denied_details()
    )