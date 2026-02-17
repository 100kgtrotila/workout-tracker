import uvicorn
from fastapi import FastAPI

from app.modules.gym.router import router as gym_router
from app.modules.user.router import router as user_router
from app.modules.training.router import router as training_router

app = FastAPI(title="Workout Tracker")
app.include_router(gym_router)
app.include_router(user_router)
app.include_router(training_router)




if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)