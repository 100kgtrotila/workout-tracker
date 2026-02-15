from typing import List

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.gym import service

from app.core.db import get_db
from app.modules.gym.schemas import ExerciseResponse, ExerciseCreate, ExerciseUpdate

router = APIRouter(prefix="/exercise", tags=["Exercise"])

@router.get("/", response_model=List[ExerciseResponse], status_code=status.HTTP_200_OK)
async def get_all_exercises(session: AsyncSession = Depends(get_db)):
    return await service.get_all_exercises(session)

@router.get("/{exercise_id}", response_model=ExerciseResponse, status_code=status.HTTP_200_OK)
async def get_exercise_by_id(exercise_id: int, session: AsyncSession = Depends(get_db)):
    return await service.get_exercise_by_id(session, exercise_id)

@router.post("/", response_model=ExerciseResponse, status_code=status.HTTP_201_CREATED)
async def create_exercise(data: ExerciseCreate, session: AsyncSession = Depends(get_db)):
    return await service.create_exercise(session, data)

@router.patch("/{exercise_id}", response_model=ExerciseResponse, status_code=status.HTTP_200_OK)
async def update_exercise(data: ExerciseUpdate, exercise_id: int, session: AsyncSession = Depends(get_db)):
    return await service.update_exercise(session, exercise_id, data)

@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(exercise_id: int, session: AsyncSession = Depends(get_db)):
    return await service.del_exercise(session, exercise_id)

