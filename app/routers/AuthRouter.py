from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.auth.jwt_utils import create_access_token
from app.db.database import get_db
from argon2 import PasswordHasher
from app.schema.loginSchema import LoginRequest, LoginResponse
from sqlalchemy.future import select
import asyncio
from datetime import datetime, timezone
import logging

router = APIRouter(prefix="/login", tags=["Auth"])
pwd_hasher = PasswordHasher()
logger = logging.getLogger(__name__)

@router.post("/local", response_model=LoginResponse)
async def login_local(login:LoginRequest, response: Response,db: AsyncSession = Depends(get_db)):
    """User sends username/password. Password is verified .  JWT token is created and stored in an HTTP-only cookie."""
    try:
        result = await db.execute(select(User).filter(User.username == login.username))
        user = result.scalars().first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        password_valid = await asyncio.to_thread(pwd_hasher.verify, user.hashed_password, login.password)
        if not password_valid:
            raise HTTPException(status_code=401, detail="Invalid password")
        
                # Update last_login
        user.last_login = datetime.now(timezone.utc)
        db.add(user)
        await db.commit()
        await db.refresh(user)

        access_token = create_access_token({"sub": str(user.id)})

        # Set secure, HTTP-only cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="None",
            path="/",
        )

        return {"message": "Login successful", "id": user.id}
    except HTTPException:
        raise
    except Exception as e:
        # Log the error 
        await db.rollback() 
        logger.exception("Login failed")
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/logout")
async def logout(response: Response):
    """Delete the cookie on client."""
    response.delete_cookie("access_token", path="/")
    return {"message": "Logged out successfully"}

# async def get_current_user(
#     request: Request,
#     db: AsyncSession = Depends(get_db)
# ):
    

#     # Fetch user from DB
#     result = await db.execute(select(User).where(User.id == user_id))
#     user = result.scalars().first()

#     if user is None:
#         raise credentials_exception

#     return user



