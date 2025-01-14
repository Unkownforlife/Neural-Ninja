import requests
import random
import string
from requests.auth import HTTPBasicAuth
from sprint_generator import generate_sprint


def create_jira_task(requirements):

    tasks = generate_sprint(requirements)
    prefix_length=4
    suffix_length=1
    prefix = ''.join(random.choices(string.ascii_uppercase, k=prefix_length))
    suffix = ''.join(random.choices(string.digits, k=suffix_length))
    key = f"{prefix}{suffix}"

    base_url = "base_url"
    url = f"{base_url}/rest/api/3/myself" 

    username = "email"
    password = "secret"

    response = requests.get(url, auth=HTTPBasicAuth(username, password))

    if response.status_code == 200:
        print("Request successful!")
        response_data = response.json()

        #create project in jira

        url = f"{base_url}/rest/api/3/project"
        payload = {
            "assigneeType": "UNASSIGNED",
            "avatarId": None,
            "categoryId": None,
            "description": tasks.get('project_objective', "project_objective"),
            "issueSecurityScheme": None,
            "key": key,
            "leadAccountId": response_data.get('accountId'),
            "name": tasks.get('project_name', "project_name"),
            "notificationScheme": None,
            "permissionScheme": None,
            "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-basic",
            "projectTypeKey": "software",
            "url": "http://atlassian.com"
        }
 
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(username, password))

        if response.status_code == 200:
            print("Project created successfully!")
            url = f"{base_url}/rest/api/3/issue"
            
            sprint_new = [{"text": sprint_goal, "type": "text"} for sprint_goal in tasks.get('sprint_goals', [])]
            payload = {
                "fields": {
                    "project": {
                    "key": key
                    },
                    "summary": "Task summary goes here",
                    "description": {
                    "content": [
                        {
                        "content": sprint_new,
                        "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                    },
                    "issuetype": {
                    "name": "Task"
                    }
                }
            }
            response = requests.post(url, json=payload, headers=headers, auth=HTTPBasicAuth(username, password))
            print(response.status_code)
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response Content:", response.text)

    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response Content:", response.text)
