from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.training.exceptions import (
    WorkoutNotFoundError,
    WorkoutSetNotFoundError,
    WorkoutExerciseNotFoundError,
)
from app.modules.training.models import Workout, WorkoutExercise, WorkoutSet
from app.modules.training.schemas import WorkoutCreate, WorkoutSetUpdate, WorkoutUpdate, WorkoutSetCreate, \
    WorkoutExerciseCreate, WorkoutExerciseUpdate


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
        .order_by(Workout.scheduled_at.desc())
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



#---------WORK OUT SETS
async def get_workout_set_by_id(
    session: AsyncSession, workout_set_id: int
) -> WorkoutSet:
    db_workout_set = await session.get(WorkoutSet, workout_set_id)

    if not db_workout_set:
        raise WorkoutSetNotFoundError(workout_set_id)

    return db_workout_set

async def create_workout_set(session: AsyncSession, workout_set_data: WorkoutSetCreate, workout_exercise_id) -> WorkoutSet:
    new_workout_set = WorkoutSet(
        reps=workout_set_data.reps,
        weight=workout_set_data.weight,
        set_number=workout_set_data.set_number,
        workout_exercise_id=workout_exercise_id
    )

    session.add(new_workout_set)
    await session.commit()
    return new_workout_set

async def update_workout_set(
    session: AsyncSession, set_id: int, update_data: WorkoutSetUpdate
) -> WorkoutSet:

    db_set = await session.get(WorkoutSet, set_id)
    if not db_set:
        raise WorkoutSetNotFoundError(set_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for k, v in update_dict.items():
        setattr(db_set, k, v)

    await session.commit()
    await session.refresh(db_set)

    return db_set

async def delete_workout_set(session: AsyncSession, db_workout_set: WorkoutSet):
    await session.delete(db_workout_set)
    await session.commit()



# -------Workout exercises

async def get_workout_exercise_by_id(session: AsyncSession, workout_exercise_id) -> WorkoutExercise:
    db_wk_e = await session.get(WorkoutExercise, workout_exercise_id)
    if not db_wk_e:
        raise WorkoutExerciseNotFoundError(workout_exercise_id)

    return db_wk_e

async def create_workout_exercise(
        session: AsyncSession, exercise_id: int, workout_id: int, data: WorkoutExerciseCreate
                                  ) -> WorkoutExercise:
    new_workout_exercise = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=data.exercise_id,
        order=data.order,
        sets=[WorkoutSet(**set_in.model_dump()) for set_in in data.sets]
    )

    session.add(new_workout_exercise)
    await session.commit()

    query = (
        select(WorkoutExercise)
        .options(selectinload(WorkoutExercise.sets))
        .where(WorkoutExercise.id == new_workout_exercise.id)
    )

    result = await session.execute(query)

    return result.scalar_one_or_none()

async def update_workout_exercise(
        session: AsyncSession, workout_exercise_id: int, update_data: WorkoutExerciseUpdate) -> WorkoutExercise:
    db_we = await session.get(WorkoutExercise, workout_exercise_id)

    if not db_we:
        raise WorkoutExerciseNotFoundError(workout_exercise_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for k, v in update_dict.items():
        setattr(db_we, k, v)

    await session.commit()
    await session.refresh(db_we)

    return db_we

async def delete_workout_exercise(session: AsyncSession, we: WorkoutExercise) -> None:
    await session.delete(we)
    await session.commit()




