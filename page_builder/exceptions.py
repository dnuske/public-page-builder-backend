from requests.exceptions import HTTPError

class Error(Exception):
  pass

class RepositoryNotFoundError(Error):
  pass

class RepositoryAlreadyExistsError(Error):
  pass

class CloudFlarePageCreationError(Error):
  def __init__(self, json, message="CloudFlare Page creation returned an error"):
    self.json = json
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f'{self.json} -> {self.message}'

class GithubRepositoryCreationError(Error):
  def __init__(self, json, message="Github repository creation returned an error"):
    self.json = json
    self.message = message
    super().__init__(self.message)

  def __str__(self):
    return f'{self.json} -> {self.message}'

