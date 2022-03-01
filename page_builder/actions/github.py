import pathlib
from dotenv import load_dotenv
import os
load_dotenv()
import uuid

GH_API_URL = "https://api.github.com/{}"

GH_API_KEY = os.getenv("GH_API_KEY")
CF_ACCOUNT_ID = os.getenv("CF_ACCOUNT_ID")
import requests
from requests.exceptions import HTTPError

import json

from page_builder.models import Page, Path
from page_builder.exceptions import *
from page_builder.custom_types import PageStatusCodes


def create_repo(repo_name, repo_description):
  response = requests.post(
    "https://api.github.com/repos/smartdataflows/sites-template/generate",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      'name': repo_name,
      'description': repo_description,
      'private': True,
      'owner': 'smartdataflows'
    }
  )

  if (response and response.status_code == 201):
    repo_data = response.json()
    return repo_data['html_url']

  if (response.status_code != 201):
    raise GithubRepositoryCreationError(response.json(),
                                        f"Github repository creation returned an error with status code {response.status_code}")


def _get_last_commit_sha(page):
  repo_name = page.github_repo.replace("https://github.com/smartdataflows/", "")
  # se obtiene el sha del ultimo commit
  response = requests.get(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/branches/master",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
  )
  return response.json()['commit']['sha']

def push_commit(page, index_file_content, generic_file_content):
  repo_name = page.github_repo.replace("https://github.com/smartdataflows/", "")

  last_sha = _get_last_commit_sha(page)

  generic_file_response = requests.post(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/git/blobs",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      'content': generic_file_content,
      'encoding': 'utf-8'
    }
  )
  generic_file_utf8_blob_sha = generic_file_response.json()['sha']

  index_file_response = requests.post(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/git/blobs",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      'content': index_file_content,
      'encoding': 'utf-8'
    }
  )
  index_file_utf8_blob_sha = index_file_response.json()['sha']

  # generar el tree de el/los archivo/s a modificar
  response = requests.post(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/git/trees",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      "base_tree": last_sha,
      "tree": [
        {
          "path": "src/pages/[...routes].js",
          "mode": "100644",
          "type": "blob",
          "sha": generic_file_utf8_blob_sha
        },
        {
          "path": "src/pages/index.js",
          "mode": "100644",
          "type": "blob",
          "sha": index_file_utf8_blob_sha
        }
      ]
    }
  )
  tree_sha = response.json()['sha']

  # generar el commit
  response = requests.post(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/git/commits",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      'message': 'Este commit fue creado por Public Page Builder',
      'author': {
        'name': 'Daniel Nuske',
        'email': 'dnuske@gmail.com'
      },
      'parents': [
        last_sha
      ],
      'tree': tree_sha
    }
  )
  new_commit_sha = response.json()['sha']

  # mover el head al nuevo commit
  response = requests.post(
    f"https://api.github.com/repos/smartdataflows/{repo_name}/git/refs/heads/master",
    headers={
      'Authorization': 'Bearer {}'.format(GH_API_KEY),
      'Accept': 'application/vnd.github.baptiste-preview+json',
      'Content-Type': 'application/json'
    },
    json={
      "ref": "refs/heads/master",
      "sha": new_commit_sha
    }
  )