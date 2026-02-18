import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_exercise(client: AsyncClient):
    # Arrange
    payload = {
        "name": "Bench Press",
        "description": "Chest exercise",
        "muscle_group": "chest"
    }

    # Act
    response = await client.post("/exercise/", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Bench Press"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_exercises(client: AsyncClient):
    await client.post("/exercise/", json={"name": "Squat", "muscle_group": "legs"})

    response = await client.get("/exercise/")
    assert response.status_code == 200
    assert len(response.json()) > 0



