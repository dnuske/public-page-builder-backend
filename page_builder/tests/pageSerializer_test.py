from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from page_builder.serializers import PageSerializer

from .factories import (
    CustomerFactory,
    PageFactory,
    PageWithForeignFactory,
    PathFactory,
)


class PageSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.page = PageWithForeignFactory.create()

    def test_that_a_page_is_correctly_serialized(self):
        page = self.page
        serializer = PageSerializer
        serialized_page = serializer(page).data

        assert serialized_page['id'] == page.id
        assert serialized_page['main_url'] == page.main_url
        assert serialized_page['cloudflare_domain'] == page.cloudflare_domain
        assert serialized_page['configuration'] == page.configuration
        assert serialized_page['github_repo'] == page.github_repo

        assert len(serialized_page['paths']) == page.paths.count()
