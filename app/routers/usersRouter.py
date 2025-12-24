from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models
from app.db.database import get_db
from app.schema import userSchema
from sqlalchemy.exc import IntegrityError

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=userSchema.UserRead)
async def create_user(user: userSchema.UserCreate, db: AsyncSession = Depends(get_db)):

    try:
        
        db_user = models.User(
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            hashed_password=user.password, 
            role=user.role
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    
    except IntegrityError as e:
        await db.rollback()
        if "users_email_key" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already registered")
        if "users_username_key" in str(e.orig):
            raise HTTPException(status_code=400, detail="Username already registered")
        raise HTTPException(status_code=400, detail="Database error")
    


@router.get("/", response_model=list[userSchema.UserRead])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.User))
    users = result.scalars().all()
    return users


