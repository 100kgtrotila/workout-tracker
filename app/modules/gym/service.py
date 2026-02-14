from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

async def get_exercise_by_id(session: AsyncSession, exercise_id: int) -> Optional[Exercise]:
    return await session.get(Exercise, exercise_id)

async def update_exercise(session:AsyncSession, db_exercise: Exercise, update_data: ExerciseUpdate) -> Exercise:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_exercise, key, value)

    await session.commit()
    await session.refresh(db_exercise)
    return db_exercise

async def del_exercise(session: AsyncSession, db_exercise: Exercise) -> None:
    await session.delete(db_exercise)
    await session.commit()
