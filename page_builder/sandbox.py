import json
from django.db.models import query
import requests
from requests.models import HTTPError

import pathlib
path = pathlib.Path(__file__).parent.resolve()

GH_API_KEY = "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"
CF_ACCOUNT_ID = "1ca6e7167d701586690ae2c73fe82121"
PROJECT_NAME = "hester"

# Obtener el sha del ultimo commit del repo
#
# GET /repos/:owner/:repo/branches/:branch_name
response = requests.get(
    "https://api.github.com/repos/smartdataflows/sites-hester/branches/master",
    headers={
        'Authorization': 'Bearer {}'.format(GH_API_KEY),
        'Accept': 'application/vnd.github.baptiste-preview+json',
        'Content-Type': 'application/json'
    },
)

print (f"Obtener ultimo commit sha: {response.status_code}")
#print (response.text)

last_sha = response.json()['commit']['sha']

# Obtener el blob del archivo 
#
# POST /repos/:owner/:repo/git/blobs
# {
#  "content": "hello world",
#  "encoding": "utf-8"
#}
file_content = open(f"{path}/[routes].js").read()
response = requests.post(
    "https://api.github.com/repos/smartdataflows/sites-hester/git/blobs",
        headers={
            'Authorization': 'Bearer {}'.format(GH_API_KEY),
            'Accept': 'application/vnd.github.baptiste-preview+json',
            'Content-Type': 'application/json'
        },
        json={
            'content': file_content,
            'encoding': 'utf-8'
        }
)

print (f"Generar blob: {response.status_code}")
#print (response.text)

utf8_blob_sha = response.json()['sha']

# Generar tree del archivo a modificar
#
# POST repos/:owner/:repo/git/trees/
# {
#   "base_tree": last_commit_sha,
#   "tree": [
#     {
#       "path": "myfolder/base64file.txt",
#       "mode": "100644",
#       "type": "blob",
#       "sha": base64_blob_sha
#     }
# }
response = requests.post(
    "https://api.github.com/repos/smartdataflows/sites-hester/git/trees",
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
            "sha": utf8_blob_sha
            }
        ]
    }
)

print (f"Generar tree: {response.status_code}")
#print (response.text)

tree_sha = response.json()['sha']

# Generar el commit
# 
# POST /repos/:owner/:repo/git/commits
# {
#   "message": "Add new files at once programatically",
#   "author": {
#     "name": "Jan-Michael Vincent",
#     "email": "JanQuadrantVincent16@rickandmorty.com"
#   },
#   "parents": [
#     last_commit_sha
#   ],
#   "tree": tree_sha
# }
response = requests.post(
    "https://api.github.com/repos/smartdataflows/sites-hester/git/commits",
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
print (f"Generar commit: {response.status_code}")

new_commit_sha = response.json()['sha']

print(f"SHA del nuevo commit: {new_commit_sha}")
#print (response.text)

# Mover el HEAD de master al nuevo commit
# 
# POST /repos/:owner/:repo/git/refs/heads/master
# {
#     "ref": "refs/heads/master",
#     "sha": new_commit_sha
# }
response = requests.post(
    "https://api.github.com/repos/smartdataflows/sites-hester/git/refs/heads/master",
    headers={
        'Authorization': 'Bearer {}'.format(GH_API_KEY),
        'Accept': 'application/vnd.github.baptiste-preview+json',
        'Content-Type':  'application/json'
    },
    json={
        "ref": "refs/heads/master",
        "sha": new_commit_sha
    }
)

print(f"Mover HEAD de master: {response.status_code}")
#print(response.text)