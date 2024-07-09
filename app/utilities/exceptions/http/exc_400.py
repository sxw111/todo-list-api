from fastapi import HTTPException, status

from app.utilities.messages.exc_details import (
    http_400_username_details,
    http_400_email_details,
    http_400_signup_credentials_details,
)


async def http_400_exc_bad_username_request(username: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_username_details(username=username),
    )


async def http_400_exc_bad_email_request(email: str) -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_email_details(email=email),
    )


async def http_exc_400_credentials_bad_signup_request() -> Exception:
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=http_400_signup_credentials_details(),
    )
