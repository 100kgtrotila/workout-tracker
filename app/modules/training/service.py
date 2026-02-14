from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.training.exceptions import WorkoutNotFoundError
from app.modules.training.models import Workout, WorkoutExercise, WorkoutSet
from app.modules.training.schemas import WorkoutCreate, WorkoutUpdate


async def get_workout_by_id(session: AsyncSession, workout_id: int, user_id: int) -> Workout:
    query = (
        select(Workout)
        .options(
            selectinload(Workout.exercises).selectinload(WorkoutExercise.sets))
            .where(Workout.id == workout_id, Workout.user_id==user_id)
        )

    result = await session.execute(query)
    workout = result.scalar_one_or_none()

    if not workout:
        raise WorkoutNotFoundError(workout_id)

    return workout


async def get_user_workouts(session: AsyncSession, user_id: int) -> List[Workout]:
    query = (
        select(Workout)
        .options(selectinload(Workout.exercises).selectinload(WorkoutExercise.sets))
        .where(Workout.user_id==user_id)
        .ordery_by(Workout.scheduled_at.desc())
    )

    result = await session.execute(query)

    return result.scalars().all()


async def create_workout(session: AsyncSession, user_id: int, workout_in: WorkoutCreate) -> Workout:
    new_workout = Workout(
        user_id=user_id,
        name=workout_in.name,
        scheduled_at=workout_in.scheduled_at,
        status=workout_in.status,
        notes=workout_in.notes,

        exercises=[
            WorkoutExercise(
                exercise_id=ex_in.exercise_id,
                order=ex_in.order,
                sets=[WorkoutSet(**set_in.model_dump()) for set_in in ex_in.sets]
            ) for ex_in in workout_in.exercises
        ]
    )

    session.add(new_workout)
    await session.commit()

    return await get_workout_by_id(session, new_workout.id, user_id)

async def update_workout_info(session: AsyncSession, db_workout: Workout, update_data: WorkoutUpdate) -> Workout:
    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_workout, key, value)

    await session.commit()
    await session.refresh(db_workout)
    return db_workout

async def del_workout(session: AsyncSession, db_workout: Workout) -> None:
    await session.delete(db_workout)
    await session.commit()




