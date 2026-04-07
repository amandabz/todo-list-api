from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserResponseToken, Token
from app.security import hash_password, create_access_token

router = APIRouter(prefix="/register", tags=["register"])

# register
@router.post("/", response_model=UserResponseToken, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # verify if the email already exists
    existing_user = db.exec(select(User).where(User.email == user_data.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un usuario con ese email"
        )

    # create the user with hashed password
    user = User(
        email=user_data.email,
        name=user_data.name,
        hashed_password=hash_password(user_data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # create and return the token
    if not user.id:
        raise HTTPException(status_code=500, detail="Error interno")

    token = create_access_token(user.id)
    return Token(token=token)
