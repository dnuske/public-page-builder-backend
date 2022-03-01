import pathlib
from dotenv import load_dotenv
import os
load_dotenv()
import requests
import uuid
from page_builder.exceptions import *

CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
CF_AUTH_EMAIL = os.getenv("CF_AUTH_EMAIL")
CF_AUTH_KEY = os.getenv("CF_ACCOUNT_KEY")

def deploy_page(page):
  response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pages/projects/{page.cloudflare_project_name}/deployments",
    headers={
      'X-Auth-Email': CF_AUTH_EMAIL,
      'X-Auth-Key': CF_AUTH_KEY,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  )

  if (response.status_code == 200):
    return True
  else:
    raise Error(response.status_code);

def create_page(page, retry_counter=0):

  response = requests.post(
    f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pages/projects",
    headers={
      'X-Auth-Email': CF_AUTH_EMAIL,
      'X-Auth-Key': CF_AUTH_KEY,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    json={
      'name': page.cloudflare_project_name,
      'build_config': {
        'build_command': 'next build && next export',
        'destination_dir': 'out',
        'root_dir': '',
      },
      'source': {
        "type": "github",
        "config": {
          "owner": "smartdataflows",
          "repo_name": page.github_repo.replace("https://github.com/smartdataflows/", ""),
          "production_branch": "master",
          "pr_comments_enabled": True,
          "deployments_enabled": True
        }
      },
      'deployment_configs': {
        "production": {
          "env_vars": {
            "BUILD_VERSION": {
              "value": "0.1"
            }
          }
        }
      }
    }
  )

  if (response.status_code == 200):
    page_data = response.json()
    return page_data['result']['subdomain']

  elif response.status_code == 409 and retry_counter < 3:
    # if the name already exists retry
    page.cloudflare_project_name += str(uuid.uuid4())[:1]
    page.save()
    return create_page(page, retry_counter+1)
  else:
    raise CloudFlarePageCreationError(response.json(),
                                      f"CloudFlare creation page returned an error with status code {response.status_code}: {response.json()}")


def deploy_status(page):

  response = requests.get(
    f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/pages/projects/{page.cloudflare_project_name}",
    headers={
      'X-Auth-Email': CF_AUTH_EMAIL,
      'X-Auth-Key': CF_AUTH_KEY,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    }
  )

  if (response.status_code == 200):
    page_data = response.json()
    return page_data['result']['latest_deployment']['latest_stage']
  else:
    raise CloudFlarePageCreationError(response.json(),
                                      f"CloudFlare creation page returned an error with status code {response.status_code}: {response.json()}")
