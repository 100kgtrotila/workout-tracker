from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.gym.exceptions import ExerciseNotFoundError
from app.modules.gym.models import Exercise
from app.modules.training.exceptions import (
    WorkoutNotFoundError,
    WorkoutSetNotFoundError,
    WorkoutExerciseNotFoundError,
)
from app.modules.training.models import Workout, WorkoutExercise, WorkoutSet
from app.modules.training.schemas import WorkoutCreate, WorkoutSetUpdate, WorkoutUpdate, WorkoutSetCreate, \
    WorkoutExerciseCreate, WorkoutExerciseUpdate


#---------WORKOUTS
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


async def get_user_workouts(session: AsyncSession, user_id: int,
                            last_workout_id: int, limit: int = 20) -> List[Workout]:
    query = (
        select(Workout)
        .options(selectinload(Workout.exercises).selectinload(WorkoutExercise.sets))
        .where(Workout.user_id == user_id)
        .order_by(Workout.id.desc())
    )

    if last_workout_id:
        query = query.where(Workout.id < last_workout_id)

    query = query.limit(limit)

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

async def update_workout_info(session: AsyncSession, user_id: int ,workout_id: int, update_data: WorkoutUpdate) -> Workout:

    db_workout = await get_workout_by_id(session, workout_id, user_id)

    if not db_workout:
        raise WorkoutNotFoundError(workout_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(db_workout, key, value)

    await session.commit()
    await session.refresh(db_workout)
    return db_workout

async def del_workout(session: AsyncSession, workout_id: int, user_id: int) -> None:

    db_workout = await get_workout_by_id(session, workout_id, user_id)

    if not db_workout:
        raise WorkoutNotFoundError(workout_id)

    await session.delete(db_workout)
    await session.commit()



#---------WORK OUT SETS
async def get_workout_set_by_id(
    session: AsyncSession, workout_set_id: int,
        user_id: int
) -> WorkoutSet:

    query = (
        select(WorkoutSet)
        .join(WorkoutExercise, WorkoutSet.workout_exercise_id == WorkoutExercise.id)
        .join(Workout, WorkoutExercise.workout_id == Workout.id)
        .where(WorkoutSet.id == workout_set_id, Workout.user_id == user_id)
    )

    result = await session.execute(query)
    db_workout_set = result.scalar_one_or_none()

    if not db_workout_set:
        raise WorkoutSetNotFoundError(workout_set_id)

    return db_workout_set

async def create_workout_set(session: AsyncSession,
                             workout_set_data: WorkoutSetCreate,
                             workout_exercise_id,
                             user_id: int) -> WorkoutSet:

    query_check = (
        select(WorkoutExercise)
        .join(Workout)
        .where(WorkoutExercise.id == workout_exercise_id,
               Workout.user_id == user_id)
    )

    result = await session.execute(query_check)
    parent_exercise = result.scalar_one_or_none()

    if not parent_exercise:
        raise WorkoutExerciseNotFoundError(workout_exercise_id)

    new_workout_set = WorkoutSet(
        reps=workout_set_data.reps,
        weight=workout_set_data.weight,
        set_number=workout_set_data.set_number,
        workout_exercise_id=workout_exercise_id
    )

    session.add(new_workout_set)
    await session.commit()
    await session.refresh(new_workout_set)
    return new_workout_set

async def update_workout_set(
    session: AsyncSession, set_id: int, update_data: WorkoutSetUpdate,
        user_id: int
) -> WorkoutSet:

    db_set = await get_workout_set_by_id(session, workout_set_id=set_id, user_id=user_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for k, v in update_dict.items():
        setattr(db_set, k, v)

    await session.commit()
    await session.refresh(db_set)

    return db_set


async def delete_workout_set(session: AsyncSession, set_id: int, user_id: int):
    db_set = await get_workout_set_by_id(session, workout_set_id=set_id, user_id=user_id)

    await session.delete(db_set)
    await session.commit()



# -------Workout exercises

async def get_workout_exercise_by_id(session: AsyncSession, workout_exercise_id, user_id: int) -> WorkoutExercise:

    query = (
        select(WorkoutExercise)
        .join(Workout, WorkoutExercise.workout_id == Workout.id)
        .where(WorkoutExercise.id == workout_exercise_id, Workout.user_id == user_id)
    )

    result = await session.execute(query)
    db_workout_exercise = result.scalar_one_or_none()

    if not db_workout_exercise:
        raise WorkoutExerciseNotFoundError(workout_exercise_id)


    return db_workout_exercise

async def create_workout_exercise(
        session: AsyncSession, user_id: int,
        workout_id: int, data: WorkoutExerciseCreate
                                  ) -> WorkoutExercise:

    exercise = await session.get(Exercise, data.exercise_id)

    if not exercise:
        raise ExerciseNotFoundError(data.exercise_id)

    workout = await get_workout_by_id(session, workout_id, user_id)

    new_workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=data.exercise_id,
        order=data.order,
        sets= [WorkoutSet(**set_in.model_dump()) for set_in in data.sets]
    )

    session.add(new_workout_exercise)
    await session.commit()
    await session.refresh(new_workout_exercise)

    return new_workout_exercise

async def update_workout_exercise(
        session: AsyncSession, workout_exercise_id: int,
        user_id: int,
        update_data: WorkoutExerciseUpdate) -> WorkoutExercise:

    db_workout_exercise = await get_workout_exercise_by_id(session, workout_exercise_id, user_id)

    update_dict = update_data.model_dump(exclude_unset=True)

    for k, v in update_dict.items():
        setattr(db_workout_exercise, k, v)

    await session.commit()
    await session.refresh(db_workout_exercise)

    return db_workout_exercise

async def delete_workout_exercise(session: AsyncSession, workout_exercise_id: int, user_id: int) -> None:
    db_workout_exercise = await get_workout_exercise_by_id(session, workout_exercise_id, user_id)

    await session.delete(db_workout_exercise)
    await session.commit()




