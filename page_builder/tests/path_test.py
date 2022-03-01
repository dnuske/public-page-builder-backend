import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Path
from .factories import CustomerFactory, PageFactory, PathFactory

faker = Factory.create()


class Path_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        PathFactory.create_batch(size=3)
        self.customer = CustomerFactory.create()
        self.page = PageFactory.create()

    def test_create_path(self):
        """
        Ensure we can create a new path object.
        """
        client = self.api_client
        path_count = Path.objects.count()
        path_dict = factory.build(dict, FACTORY_CLASS=PathFactory,
                                  customer=self.customer.id, page=self.page.id)
        response = client.post(reverse('path-list'), path_dict)
        created_path_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Path.objects.count() == path_count + 1
        path = Path.objects.get(pk=created_path_pk)

        assert path_dict['path'] == path.path
        assert path_dict['json_content'] == path.json_content

    def test_get_one(self):
        client = self.api_client
        path_pk = Path.objects.first().pk
        path_detail_url = reverse('path-detail', kwargs={'pk': path_pk})
        response = client.get(path_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('path-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Path.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        path_qs = Path.objects.all()
        path_count = Path.objects.count()

        for i, path in enumerate(path_qs, start=1):
            response = client.delete(reverse('path-detail', kwargs={'pk': path.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert path_count - i == Path.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        path_pk = Path.objects.first().pk
        path_detail_url = reverse('path-detail', kwargs={'pk': path_pk})
        path_dict = factory.build(dict, FACTORY_CLASS=PathFactory,
                                  customer=self.customer.id, page=self.page.id)
        response = client.patch(path_detail_url, data=path_dict)
        assert response.status_code == status.HTTP_200_OK

        assert path_dict['path'] == response.data['path']
        assert path_dict['json_content'] == response.data['json_content']

    def test_update_path_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        path = Path.objects.first()
        path_detail_url = reverse('path-detail', kwargs={'pk': path.pk})
        path_path = path.path
        data = {
            'path': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(path_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert path_path == Path.objects.first().path

    def test_update_json_content_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        path = Path.objects.first()
        path_detail_url = reverse('path-detail', kwargs={'pk': path.pk})
        path_json_content = path.json_content
        data = {
            'json_content': faker.pystr(min_chars=65536, max_chars=65536),
        }
        response = client.patch(path_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert path_json_content == Path.objects.first().json_content
