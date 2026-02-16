from typing import List

from fastapi import status, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.core.security import get_current_user
from app.modules.training import service
from app.core.db import get_db
from app.modules.training.schemas import (
    WorkoutResponse,
    WorkoutCreate,
    WorkoutUpdate,
    WorkoutSetResponse,
    WorkoutSetCreate,
    WorkoutSetUpdate,
)
from app.modules.user.models import User

router = APIRouter(prefix="/training", tags=["training"])

#WORKOUTS

@router.get("/workout/{workout_id}", response_model=WorkoutResponse, status_code=status.HTTP_200_OK)
async def get_workout_by_id(workout_id: int, session: AsyncSession = Depends(get_db),
                            current_user: User = Depends(get_current_user)):
    return await service.get_workout_by_id(session, workout_id, current_user.id)

@router.get("/workout/user", response_model=List[WorkoutResponse], status_code=status.HTTP_200_OK)
async def get_user_workouts(last_workout: int | None = None,
        limit: int = 20,
        session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    workouts = await service.get_user_workouts(
        session,
        user_id=current_user.id,
        last_workout_id=last_workout,
        limit=limit)

    return workouts

@router.post("/workout", response_model=WorkoutResponse, status_code=status.HTTP_201_CREATED)
async def create_workout(workout_data: WorkoutCreate, session: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):
    return await service.create_workout(session, user_id=current_user.id, workout_in=workout_data)

@router.patch("/workout/{workout_id}", response_model=WorkoutResponse, status_code=status.status.HTTP_200_OK)
async def update_workout(workout_id: int, update_data: WorkoutUpdate, session: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):

    return await service.update_workout_info(session, workout_id=workout_id,
                                             update_data=update_data, user_id=current_user.id)

@router.delete("/workout/{workout_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout(workout_id: int, session: AsyncSession = Depends(get_db),
                         current_user: User = Depends(get_current_user)):

    return await service.del_workout(session, workout_id=workout_id, user_id=current_user.id)

#WORKOUT SETS

@router.get("/workout_set/{workout_set_id}", response_model=WorkoutSetResponse, status_code=status.HTTP_200_OK)
async def get_workout_set(workout_set_id: int, session: AsyncSession = Depends(get_db)):
    return await service.get_workout_set_by_id(session, workout_set_id)

@router.post("/workout_set/", response_model=WorkoutSetResponse, status_code=status.HTTP_201_CREATED)
async def create_workout_set(workout_set_data: WorkoutSetCreate,
                             workout_exercise_id: int,
                             session: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    return await service.create_workout_set(session, workout_set_data=workout_set_data,
                                            workout_exercise_id=workout_exercise_id,
                                            user_id=current_user.id)

@router.patch("/workout_set/{workout_set_id}", response_model=WorkoutSetResponse, status_code=status.HTTP_200_OK)
async def update_workout_set(set_id: int, update_data: WorkoutSetUpdate,
                             session: AsyncSession = Depends(get_db),
                             current_user = Depends(get_current_user)):

    return await service.update_workout_set(session, set_id=set_id, update_data=update_data, user_id=current_user.id)

@router.delete("/workout_set/{workout_set_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workout_set(set_id: int, session: AsyncSession = Depends(get_db),
                             current_user: User = Depends(get_current_user)):

    return await service.delete_workout_set(session, set_id=set_id, user_id=current_user.id)






