from app.schema.auth import LoginRequest
from fastapi import APIRouter, HTTPException, status

auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/login")
def login(body: LoginRequest):

    email = body.email
    password = body.password

    if email != "admin@admin.com":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email not found"
        )

    if password != "admin123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password"
        )

    return {"message": "Good!"}
