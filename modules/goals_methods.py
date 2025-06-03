import requests
from faker import Faker
fake = Faker()

BASE_URL = "https://api.clickup.com/api/v2"
TEAM_ID = "90151251321"

goals_url = f"{BASE_URL}/team/{TEAM_ID}/goal"
my_headers = {"Authorization": "pk_200564658_TNOBEQYDGC5SS4JX7H02H9KOR1OQWRR2"}
invalid_token = {"Authorization": "pk_200437946oooo"}
empty_token = {"Authorization": ""}


def create_goal(headers=None, team_id=None):
    custom_headers = headers or my_headers
    team_id = team_id or TEAM_ID
    random_name = fake.first_name()
    body = {
        "name": random_name
    }
    return requests.post(f"https://api.clickup.com/api/v2/team/{team_id}/goal", headers=custom_headers, json=body)

def get_all_goals(headers=None, team_id=None):
    return requests.get(f"https://api.clickup.com/api/v2/team/{team_id}/goal", headers=headers)

def get_goal(goal_id, headers=None):
    custom_headers = headers or my_headers
    return requests.get(f"https://api.clickup.com/api/v2/goal/{goal_id}", headers=custom_headers)


# def update_goal(goal_id=None, headers=None):
#     custom_headers = headers or my_headers
#     random_name_for_update = fake.first_name()
#     body_updated = {
#         "name": random_name_for_update
#     }
#     return requests.put("https://api.clickup.com/api/v2/goal/" + goal_id, headers=custom_headers, json=body_updated)


def update_goal(goal_id, name=None, description=None, headers=None):
    custom_headers = headers or my_headers
    body = {}
    if name is not None:
        body["name"] = name
    if description is not None:
        body["description"] = description

    response = requests.put(f"https://api.clickup.com/api/v2/goal/{goal_id}", headers=custom_headers, json=body)

    return response, body

def delete_goal(goal_id=None, headers=None):
    custom_headers = headers or my_headers
    return requests.delete("https://api.clickup.com/api/v2/goal/" + goal_id, headers=custom_headers)