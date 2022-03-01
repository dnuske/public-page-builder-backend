import pathlib
import uuid
import requests
from requests.exceptions import HTTPError

import json

from page_builder.models import Page, Path
from page_builder.exceptions import *
from page_builder.custom_types import PageStatusCodes
from page_builder.actions import github, cloudflare


def trigger_page_deploy(page):
    if (not page.cloudflare_domain or not page.github_repo):
        raise Error("No cumple los requisitos. Verifique que tenga configurado un repositorio y una pagina de CloudFlare")

    return cloudflare.deploy_page(page)


def create_cloudflare_page(page):
  try:
    page.status_code = PageStatusCodes.CREATING_PAGE_STARTED.value
    page.save()
    _create_cloudflare_page(page)
    page.status_code = PageStatusCodes.CREATING_PAGE_SUCCESS.value
    page.save()
  except RepositoryNotFoundError:
    page.status_code = PageStatusCodes.CREATING_PAGE_FAILURE.value
    page.status_message = "Repositorio en GitHub no definido. Establezca el repositorio a usar primero"
    page.save()
    raise
  except Exception as e:
    page.status_code = PageStatusCodes.CREATING_PAGE_FAILURE.value
    page.status_message = e.message
    page.save()
    raise


def _create_cloudflare_page(page):
    if (not page.github_repo):
        raise RepositoryNotFoundError()

    page.cloudflare_project_name = page.name.replace(' ', '-')
    page.save()

    page.cloudflare_domain = cloudflare.create_page(page)
    page.save()
    return True

def create_github_repository(page):
  try:
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_STARTED.value
    page.save()
    _create_github_repository(page)
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_SUCCESS.value
    page.save()
  except RepositoryAlreadyExistsError:
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_FAILURE.value
    page.status_message = "Ya existe un repoitorio con ese nombre"
    page.save()
    raise
  except GithubRepositoryCreationError as e:
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_FAILURE.value
    page.status_message = "\n".join(e.json['errors'])
    page.save()
    raise
  except HTTPError as http_err:
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_FAILURE.value
    page.status_message = f'HTTP error: {http_err}'
    page.save()
    raise
  except Exception as err:
    page.status_code = PageStatusCodes.CREATING_REPOSITORY_FAILURE.value
    page.status_message = f"Hubo un error al establecer la petición HTTP: {err}"
    page.save()
    raise


def _create_github_repository(page):
    if (page.github_repo):
      raise RepositoryAlreadyExistsError()

    repo_name = f"sites-{page.name}-{str(uuid.uuid4())[:4]}".lower()
    repo_description = "{} html renderer".format(page.name).capitalize()

    page.github_repo = github.create_repo(repo_name, repo_description)
    page.save()

def push_to_repository(page):
  # obtener todos los paths y el value de cada uno
  paths = Path.objects.filter(page=page.id)
  # armar el archivo [...routes].js
  case_template = """
    case "[% route %]":
      return {
        props: {
          title: "[% title %]",
          value: [% content %]
        }
      }
  """

  paths_template = '{params: {routes: [% route %]}},\n'

  case_template_collection = ""
  paths_template_collection = ''


  for path in [p for p in paths if p.path != '/']:
    p = path.path.split('/')[1:]

    template_copy = case_template
    template_copy = template_copy.replace("[% route %]", '/'.join(p))
    template_copy = template_copy.replace("[% title %]", page.name + ' | ' + ' - '.join(p))
    template_copy = template_copy.replace("[% content %]", path.json_content)
    case_template_collection += template_copy

    template_copy = paths_template
    template_copy = template_copy.replace("[% route %]", str(p))
    paths_template_collection += template_copy

  # armar el archivo globalConf.js


  # se sube el contenido del archivo y se obitene el sha del blob
  source_file_path = pathlib.Path(__file__).parent.resolve()
  file_content = open(f"{source_file_path}/../deploy_sources/[...routes].js").read()

  file_content = file_content.replace("[% path_collection %]", paths_template_collection)
  file_content = file_content.replace("[% template_collection %]", case_template_collection)


  p = [p for p in paths if p.path == '/'][0]
  index_template = """
    props: {
      title: "[% title %]",
      value: [% content %]
    }
  """
  index_template = index_template.replace("[% title %]", page.name + '|' + p.path)
  index_template = index_template.replace("[% content %]", p.json_content)

  index_file_content = open(f"{source_file_path}/../deploy_sources/index.js").read()
  index_file_content = index_file_content.replace("[% template_data %]", index_template)

  github.push_commit(page, index_file_content, file_content)

def get_deploy_status(page):
  d = cloudflare.deploy_status(page)
  res = {
    'deploy_status': d['status'],
    'deploy_date_started': d['started_on'],
    'deploy_date_ended': d['ended_on']
  }
  page.deploy_status = res['deploy_status']
  page.deploy_date_started = res['deploy_date_started']
  page.deploy_date_ended = res['deploy_date_ended']
  page.save()
  return res

