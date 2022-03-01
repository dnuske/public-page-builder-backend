from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from page_builder.serializers import PathSerializer

from .factories import PathFactory


class PathSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.path = PathFactory.create()

    def test_that_a_path_is_correctly_serialized(self):
        path = self.path
        serializer = PathSerializer
        serialized_path = serializer(path).data

        assert serialized_path['id'] == path.id
        assert serialized_path['path'] == path.path
        assert serialized_path['json_content'] == path.json_content
