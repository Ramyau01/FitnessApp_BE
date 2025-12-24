from __future__ import annotations
from sqlalchemy import  String, TIMESTAMP, Boolean, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.db.base import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID



class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    unique=True,
    nullable=False
)
    email : Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    username : Mapped[str]  = mapped_column(String(45), unique=True, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    phone_number: Mapped[Optional[str]] = mapped_column(String(15), nullable=True)
    hashed_password :Mapped[str] = mapped_column(String(200),  nullable=False)
    is_active: Mapped[bool]  = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False )
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    created_at: Mapped[datetime]= mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    #Relationship
    workout_plans: Mapped[List["WorkoutPlan"]] = relationship( "WorkoutPlan",
    back_populates="coach",
    cascade="all, delete-orphan"
)