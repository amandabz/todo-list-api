from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models import User
from app.schemas import UserLogin, Token
from app.security import verify_password, create_access_token

router = APIRouter(prefix="/login", tags=["login"])

# login
@router.post("/", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # search user by email
    user = db.exec(select(User).where(User.email == user_data.email)).first()

    # verify if users already exists and if the password is correct
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )

    # create and return the token
    if not user.id:
        raise HTTPException(status_code=500, detail="Error interno")

    token = create_access_token(user.id)
    return Token(token=token)
