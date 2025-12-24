from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import usersRouter, AuthRouter
from app.db.database import engine, Base
# from app.core.logfire_config import  logger
# import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup: create tables ---
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized")

    yield  # App runs here

    # --- Shutdown (optional): clean up ---
    await engine.dispose()
    print("🧹 Database connection closed")

# Create the FastAPI app WITH lifespan
app = FastAPI(title="Fitness App", lifespan=lifespan)

# Register routers AFTER app is created
app.include_router(usersRouter.router)
app.include_router(AuthRouter.router)
 # Register routers
# app.include_router(user_router, prefix="/users", tags=["Users"])
# app.include_router(workout_router, prefix="/workouts", tags=["Workouts"])

# Initialize DB on startup
# @app.on_event("startup")
# async def on_startup():
#     await init_db()


# Enable API request logging only in production
# if os.getenv("ENVIRONMENT", "production").lower() == "production":
#     @app.middleware("http")
#     async def log_requests(request: Request, call_next):
#         logger.info(f"➡️  Request: {request.method} {request.url}")
#         response = await call_next(request)
#         logger.info(f"⬅️  Response: {request.method} {request.url} — {response.status_code}")
#         return response