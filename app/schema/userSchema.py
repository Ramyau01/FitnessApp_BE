from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
import re
from typing import Annotated
# from passlib.hash import argon2
from argon2 import PasswordHasher
from datetime import datetime
import uuid

#EmailStr - ensures email format, domain name exists, string like type, EmailStr does NOT normalize (lowercase/strip)

ALLOWED_ROLES = {"admin", "coach", "user"} 
phone_regex = re.compile(r"^\+?[0-9\-() ]+$")
pwd_hasher = PasswordHasher()

Email = Annotated[EmailStr, Field(..., max_length=200, description="User Email ID")]

UserName = Annotated[str, Field(...,min_length=2, max_length=45, description="User login name")]
LastName = Annotated[str | None, Field( max_length=45, description="User last name")]
FirstName = Annotated[str | None, Field(max_length=45, description="User first name")]
Role =  Annotated[str, Field(...,description="User Role" )]
PhoneNumber = Annotated[str, Field(min_length=7, max_length=15, pattern=r"^\+?[0-9\-() ]+$", description="User Phone Number")]

class UserBase(BaseModel):
    email: Email
    username: UserName
    first_name:  FirstName = None
    last_name:  LastName = None
    role: Role
    phone_number : PhoneNumber = None

    model_config = ConfigDict(str_strip_whitespace=True)

    # Email normalization
    @field_validator("email")
    def normalize_email(cls, v):
        return v.lower()
    
    # Role validation
    @field_validator("role")
    def validate_role(cls, v):
        if v not in ALLOWED_ROLES:
            raise ValueError(f"role must be one of: {ALLOWED_ROLES}")
        return v
    
    # Phone normalization
    @field_validator("phone_number")
    def normalize_phone(cls, v):
        if v is None:
            return v
        v = v.strip().replace(" ", "")
        if not phone_regex.fullmatch(v):
            raise ValueError("Invalid phone number format")
        return v  
    


class UserCreate(UserBase):
    password: str = Field(..., min_length=7, max_length=72)

# Hash password after validation
    @field_validator("password", mode="after")
    def hash_password(cls, password, info):
        username = info.data.get("username")
        if username and password and username == password :
            raise ValueError("Password cannot be the same as username")
        #password hashing
       
        return pwd_hasher.hash(password)
    

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    first_name: str | None
    last_name: str | None
    role: str
    phone_number: str | None
    is_active: bool
    is_verified: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
    last_login : Annotated[datetime | None, Field( description="User last login time")]

    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode = True



#          hashed_password :Mapped[str] = mapped_column(String(200),  nullable=False)
#     is_active: Mapped[bool]  = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False )
#     is_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
#     created_at: Mapped[datetime]= mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
#     updated_at: Mapped[datetime] = mapped_column(
#         TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
#     )
#     last_login: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    
#     role: Mapped[str] = mapped_column(String(20), nullable=False)
#     is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
# #Relationship
