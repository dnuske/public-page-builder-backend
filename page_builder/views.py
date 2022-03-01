from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Page, Path
from .serializers import PageSerializer, PathSerializer
from page_builder.custom_types import PageStatusCodes
from page_builder.exceptions import *
from page_builder.actions import create_github_repository, create_cloudflare_page, trigger_page_deploy, push_to_repository, get_deploy_status

class PathViewSet(viewsets.ModelViewSet):
    queryset = Path.objects.all()
    serializer_class = PathSerializer
    permission_classes = []
    filterset_fields = ['id', 'path', 'json_content', 'user', 'page']
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    permission_classes = []
    filterset_fields = ['id', 'main_url', 'cloudflare_domain',
                        'configuration', 'github_repo', 'paths', 'user']
    def perform_create(self, serializer):
      serializer.save(user=self.request.user)

    @action(detail=True)
    def initial_setup(self, request, pk):
      page = Page.objects.get(pk=pk)

      if page.status_code == PageStatusCodes.INITIAL.value:
        try:
          create_github_repository(page)
        except Exception as e:
          print(' error ', e)
          return Response(str(e), 500)

      if page.status_code == PageStatusCodes.CREATING_REPOSITORY_SUCCESS.value:
        try:
          create_cloudflare_page(page)
        except Exception as e:
          print(' error ', e)
          return Response(str(e), 500)

      page.deploy_status = 'idle'
      page.save()
      return Response(f'Initial_setup for {pk} - {page.name} completed')

    @action(detail=True)
    def deploy(self, request, pk):
      page = Page.objects.get(pk=pk)

      if page.status_code in (PageStatusCodes.CREATING_PAGE_SUCCESS.value, PageStatusCodes.DEPLOYING_SUCCESS.value):
        try:
          trigger_page_deploy(page)
        except Exception as e:
          print(' error ', e)
          return Response(str(e), 500)
        return Response(f'Initial_setup for {pk} - {page.name} completed')
      else:
        return Response(f'Wrong status, please contact support', 500)

    @action(detail=True)
    def push_changes(self, request, pk):
      page = Page.objects.get(pk=pk)
      page.deploy_status = 'active'
      page.save()

      try:
        push_to_repository(page)
      except Exception as e:
        print(' error ', e)
        raise
        #return Response(str(e), 500)
      return Response(f'push_to_repository for {pk} - {page.name} completed')


    @action(detail=True)
    def deploy_status(self, request, pk):
      page = Page.objects.get(pk=pk)

      res = get_deploy_status(page)
      return Response(res)

    @action(detail=True)
    def deploy_status_to_idle(self, request, pk):
      page = Page.objects.get(pk=pk)
      page.deploy_status = 'idle'
      page.save()
      return Response(True)

