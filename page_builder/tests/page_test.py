import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Page
from .factories import CustomerFactory, PageFactory, PathFactory

faker = Factory.create()


class Page_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        PageFactory.create_batch(size=3)
        self.customer = CustomerFactory.create()

    def test_create_page(self):
        """
        Ensure we can create a new page object.
        """
        client = self.api_client
        page_count = Page.objects.count()
        page_dict = factory.build(dict, FACTORY_CLASS=PageFactory, customer=self.customer.id)
        response = client.post(reverse('page-list'), page_dict)
        created_page_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Page.objects.count() == page_count + 1
        page = Page.objects.get(pk=created_page_pk)

        assert page_dict['main_url'] == page.main_url
        assert page_dict['cloudflare_domain'] == page.cloudflare_domain
        assert page_dict['configuration'] == page.configuration
        assert page_dict['github_repo'] == page.github_repo

    def test_get_one(self):
        client = self.api_client
        page_pk = Page.objects.first().pk
        page_detail_url = reverse('page-detail', kwargs={'pk': page_pk})
        response = client.get(page_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('page-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Page.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        page_qs = Page.objects.all()
        page_count = Page.objects.count()

        for i, page in enumerate(page_qs, start=1):
            response = client.delete(reverse('page-detail', kwargs={'pk': page.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert page_count - i == Page.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        page_pk = Page.objects.first().pk
        page_detail_url = reverse('page-detail', kwargs={'pk': page_pk})
        page_dict = factory.build(dict, FACTORY_CLASS=PageFactory, customer=self.customer.id)
        response = client.patch(page_detail_url, data=page_dict)
        assert response.status_code == status.HTTP_200_OK

        assert page_dict['main_url'] == response.data['main_url']
        assert page_dict['cloudflare_domain'] == response.data['cloudflare_domain']
        assert page_dict['configuration'] == response.data['configuration']
        assert page_dict['github_repo'] == response.data['github_repo']

    def test_update_main_url_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        page = Page.objects.first()
        page_detail_url = reverse('page-detail', kwargs={'pk': page.pk})
        page_main_url = page.main_url
        data = {
            'main_url': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(page_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert page_main_url == Page.objects.first().main_url

    def test_update_cloudflare_domain_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        page = Page.objects.first()
        page_detail_url = reverse('page-detail', kwargs={'pk': page.pk})
        page_cloudflare_domain = page.cloudflare_domain
        data = {
            'cloudflare_domain': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(page_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert page_cloudflare_domain == Page.objects.first().cloudflare_domain

    def test_update_configuration_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        page = Page.objects.first()
        page_detail_url = reverse('page-detail', kwargs={'pk': page.pk})
        page_configuration = page.configuration
        data = {
            'configuration': faker.pystr(min_chars=65536, max_chars=65536),
        }
        response = client.patch(page_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert page_configuration == Page.objects.first().configuration

    def test_update_github_repo_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        page = Page.objects.first()
        page_detail_url = reverse('page-detail', kwargs={'pk': page.pk})
        page_github_repo = page.github_repo
        data = {
            'github_repo': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(page_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert page_github_repo == Page.objects.first().github_repo
