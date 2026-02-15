from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.gym.exceptions import ExerciseNotFoundError
from app.modules.gym.models import Exercise
from app.modules.gym.schemas import ExerciseCreate, ExerciseUpdate


async def create_exercise(session: AsyncSession, exercise_in: ExerciseCreate) -> Exercise:
    new_exercise = Exercise(**exercise_in.model_dump())

    session.add(new_exercise)
    await session.commit()
    await session.refresh(new_exercise)

    return new_exercise

async def get_all_exercises(session: AsyncSession) -> List[Exercise]:
    query = select(Exercise).order_by(Exercise.name)
    result = await session.execute(query)
    return result.scalars().all()


async def get_exercise_by_id(session: AsyncSession, exercise_id: int) -> Exercise:
    db_exercise = await session.get(Exercise, exercise_id)
    if not db_exercise:
        raise ExerciseNotFoundError(exercise_id)
    return db_exercise

async def update_exercise(session:AsyncSession, exercise_id: int, update_data: ExerciseUpdate) -> Exercise:
    update_dict = update_data.model_dump(exclude_unset=True)

    db_exercise = await session.get(exercise_id)

    if not db_exercise:
        raise ExerciseNotFoundError(exercise_id)

    for key, value in update_dict.items():
        setattr(db_exercise, key, value)

    await session.commit()
    await session.refresh(db_exercise)
    return db_exercise

async def del_exercise(session: AsyncSession, exercise_id: int) -> None:
    db_exercise = await session.get(exercise_id)

    if not db_exercise:
        raise ExerciseNotFoundError(exercise_id)

    await session.delete(db_exercise)
    await session.commit()
