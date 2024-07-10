from fastapi import APIRouter, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from app.api.deps import SessionDep
from app.models.schemas.user import UserCreate, UserOut
from app.models.schemas.jwt_token import TokenResponse
from app.core.security import create_access_token
from app.utilities.exceptions.http.exc_400 import (
    http_400_exc_bad_email_request,
    http_400_exc_bad_username_request,
    http_exc_400_credentials_bad_signup_request,
)
from app.utilities.exceptions.database import EntityAlreadyExists
from app.crud.user import is_email_taken, is_username_taken, create_user, authenticate


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

    return new_user


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

    return TokenResponse(access_token=access_token, token_type="bearer")
