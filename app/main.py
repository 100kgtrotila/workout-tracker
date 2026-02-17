from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.core.config import settings
from app.modules.gym.router import router as gym_router
from app.modules.user.router import router as user_router
from app.modules.training.router import router as training_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=False,
    )

    app.state.db_engine = engine
    app.state.db_sessionmaker = session_maker

    yield

    await engine.dispose()

def create_app() -> FastAPI:
    app = FastAPI(title="WorkoutTracker", lifespan=lifespan)

    app.include_router(gym_router)
    app.include_router(user_router)
    app.include_router(training_router)

    return app
app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)