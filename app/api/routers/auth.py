from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.api.deps import SessionDep
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.crud.user import (
    authenticate,
    create_user,
    is_email_taken,
    is_username_taken,
)
from app.models.schemas.jwt_token import TokenResponse
from app.models.schemas.user import UserCreate, UserOut
from app.utilities.exceptions.database import EntityAlreadyExists
from app.utilities.exceptions.http.exc_400 import (
    http_400_exc_bad_email_request,
    http_400_exc_bad_username_request,
    http_exc_400_credentials_bad_signup_request,
)


router = APIRouter()


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(db: SessionDep, user: UserCreate) -> UserOut:
    try:
        await is_username_taken(db=db, username=user.username)
    except EntityAlreadyExists:
        raise await http_400_exc_bad_username_request(username=user.username)

    try:
        await is_email_taken(db=db, email=user.email)
    except EntityAlreadyExists:
        raise await http_400_exc_bad_email_request(email=user.email)

    new_user = await create_user(db=db, user=user)

    return new_user  # type: ignore


@router.post("/signin", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def signin(
    db: SessionDep, user_credentials: OAuth2PasswordRequestForm = Depends()
) -> TokenResponse:
    try:
        user = await authenticate(
            db=db, email=user_credentials.username, password=user_credentials.password
        )
    except Exception:
        raise await http_exc_400_credentials_bad_signup_request()

    access_token = create_access_token(data={"user_id": user.id})
    refresh_token = create_refresh_token(data={"user_id": user.id})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_TOKEN_SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: int | None = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        new_access_token = create_access_token(data={"user_id": user_id})
        new_refresh_token = create_refresh_token(data={"user_id": user_id})

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
