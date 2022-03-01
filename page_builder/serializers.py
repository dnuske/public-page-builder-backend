from rest_framework import serializers

from .models import Page, Path


class PathSerializer(serializers.ModelSerializer):
  class Meta:
    model = Path
    fields = ['id', 'path', 'json_content', 'page']
    read_only_fields = ('created', 'updated', 'user')


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'name', 'main_url', 'cloudflare_domain',
                  'configuration', 'github_repo', 'status_code', 'status_message', 'deploy_status', 'deploy_date_started', 'deploy_date_ended']
        read_only_fields = ('created', 'updated', 'user')


