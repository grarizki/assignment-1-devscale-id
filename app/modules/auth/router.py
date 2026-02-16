from app.modules.auth.utils import hash_password, verify_password
from app.models.database import User
from app.models.engine import db_session
from sqlmodel import Session, select
from app.modules.auth.schema import RegisterUser, LoginUser
from fastapi import APIRouter, Depends, HTTPException, status

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post(path="/register")
def register_user(body: RegisterUser, db: Session = Depends(dependency=db_session)):

    hashed_password: str = hash_password(plain_password=body.password)
    new_user = User(name=body.name, email=body.email, password=hashed_password)
    db.add(instance=new_user)
    db.commit()

    return {"message": "User register success!"}


@auth_router.post(path="/login")
def login_user(body: LoginUser, db: Session = Depends(dependency=db_session)):

    user: User | None = db.exec(
        statement=select(User).where(User.email == body.email)
    ).first()
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")

    if not verify_password(plain_password=body.password, hashed_password=user.password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials!")

    # Give token / access

    return {"message": "User login success!!"}
