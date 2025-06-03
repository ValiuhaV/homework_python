import uuid

import pytest
import requests

from faker import Faker
fake = Faker()
from pytest_steps import test_steps

from modules.goals_methods import (create_goal, update_goal, my_headers, invalid_token, empty_token,
                                   delete_goal, get_goal, TEAM_ID, get_all_goals)


@pytest.mark.parametrize(
    "headers, team_id, status",
    [
        (my_headers, TEAM_ID, 200),
        (my_headers, 'jhdbhjbdd', 400),
        (invalid_token, TEAM_ID, 401),
        (empty_token, TEAM_ID, 400),
    ],
    ids=[
        "valid header and team_id",
        "invalid team_id",
        "invalid token",
        "empty token"
    ]
)
def test_get_all_goals(headers, team_id, status):
    result = get_all_goals(headers=headers, team_id=team_id)
    assert result.status_code == status

# ------

@test_steps("Create new goal", "Get created goal", "Delete goal")
def test_create_goal():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@pytest.mark.parametrize(
    "headers, team_id, status",
    [
        (my_headers, 'jhdbhjbdd', 400),
        (invalid_token, TEAM_ID, 401),
        (empty_token, TEAM_ID, 400),
    ],
    ids=[
        "invalid team_id",
        "invalid token",
        "empty token"
    ]
)
def test_create_goal_failure(headers, team_id, status):
    result = create_goal(headers=headers, team_id=team_id)
    assert result.status_code == status


@test_steps("Create new goal", "Get created goal", "Delete goal")
def test_get_goal():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not get goal with invalid token", "Delete goal")
def test_get_goal_invalid_token():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = get_goal(goal_id, headers=invalid_token)
    assert result.status_code == 401
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not get goal with no token", "Delete goal")
def test_get_goal_no_token():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = get_goal(goal_id, headers=empty_token)
    assert result.status_code == 400
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not get goal with invalid goal_id", "Delete goal")
def test_get_goal_invalid_goal_id():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = get_goal(uuid.uuid4())
    assert result.status_code == 404
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield

@test_steps("Create new goal", "Update goal name", "Get updated goal", "Delete goal")
def test_update_goal_valid1():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    new_name = fake.first_name()
    response, body = update_goal(goal_id=goal_id, name=new_name)
    assert response.status_code == 200
    assert body["name"] == new_name
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield

@test_steps("Create new goal", "Update goal description", "Get updated goal", "Delete goal")
def test_update_goal_valid2():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    new_description = fake.sentence()
    response, body = update_goal(goal_id=goal_id, description=new_description)
    assert response.status_code == 200
    assert body["description"] == new_description
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not update goal with invalid token", "Check that goal name is not changed", "Delete goal")
def test_update_goal_with_invalid_token():

    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    original_name = result.json()["goal"]["name"]
    assert result.status_code == 200
    yield


    response, _ = update_goal(goal_id=goal_id, name="Тестова назва", headers=invalid_token)
    assert response.status_code == 401
    yield


    result = get_goal(goal_id)
    assert result.status_code == 200
    current_name = result.json()["goal"]["name"]
    assert current_name == original_name, f"Expected name '{original_name}', but got '{current_name}'"
    yield


    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not update goal with no token", "Check that goal name is not changed", "Delete goal")
def test_update_goal_with_no_token():

    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    original_name = result.json()["goal"]["name"]
    assert result.status_code == 200
    yield


    response, _ = update_goal(goal_id=goal_id, name="Тестова назва2", headers=empty_token)
    assert response.status_code == 400
    yield


    result = get_goal(goal_id)
    assert result.status_code == 200
    current_name = result.json()["goal"]["name"]
    assert current_name == original_name, f"Expected name '{original_name}', but got '{current_name}'"
    yield


    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield


@test_steps("Create new goal", "Should not update goal with empty goal_id", "Check that goal name is not changed", "Delete goal")
def test_update_goal_with_empty_goal_id():

    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    original_name = result.json()["goal"]["name"]
    assert result.status_code == 200
    yield

    empty_goal_id = ""
    response, _ = update_goal(goal_id=empty_goal_id, name="Нова назва")
    assert response.status_code == 404
    yield


    result = get_goal(goal_id)
    assert result.status_code == 200
    current_name = result.json()["goal"]["name"]
    assert current_name == original_name, f"Expected name '{original_name}', but got '{current_name}'"
    yield


    result = delete_goal(goal_id)
    assert result.status_code == 200
    yield

@test_steps("Create new goal", "Delete created goal", "Get deleted goal",)
def test_delete_goal():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id)
    assert result.status_code == 200
    assert result.json() == {}
    yield

    result = get_goal(goal_id)
    assert result.status_code == 404
    yield

@test_steps("Create new goal", "Should not delete goal with empty goal_id", "Check that goal is not deleted")
def test_delete_goal_with_empty_goal_id():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    empty_goal_id = ""
    response, _ = update_goal(goal_id=empty_goal_id, name="Нова назва")
    assert response.status_code == 404
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

@test_steps("Create new goal", "Should not delete goal with no token", "Check that goal is not deleted")
def test_delete_goal_with_empty_token():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id, headers=empty_token)
    assert result.status_code == 400
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield

@test_steps("Create new goal", "Should not delete goal with no token", "Check that goal is not deleted")
def test_delete_goal_with_invalid_goal():
    result = create_goal()
    goal_id = result.json()["goal"]["id"]
    assert result.status_code == 200
    yield

    result = delete_goal(goal_id, headers=invalid_token)
    assert result.status_code == 401
    yield

    result = get_goal(goal_id)
    assert result.status_code == 200
    yield