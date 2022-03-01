import json
from datetime import datetime

import factory
from django.core import management
from django.test import TestCase
from django.urls import reverse
from faker import Factory
from rest_framework import status
from rest_framework.test import APIClient

from ..models import Customer
from .factories import CustomerFactory, PageFactory, PathFactory

faker = Factory.create()


class Customer_Test(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        CustomerFactory.create_batch(size=3)

    def test_create_customer(self):
        """
        Ensure we can create a new customer object.
        """
        client = self.api_client
        customer_count = Customer.objects.count()
        customer_dict = factory.build(dict, FACTORY_CLASS=CustomerFactory)
        response = client.post(reverse('customer-list'), customer_dict)
        created_customer_pk = response.data['id']
        assert response.status_code == status.HTTP_201_CREATED
        assert Customer.objects.count() == customer_count + 1
        customer = Customer.objects.get(pk=created_customer_pk)

        assert customer_dict['email'] == customer.email

    def test_get_one(self):
        client = self.api_client
        customer_pk = Customer.objects.first().pk
        customer_detail_url = reverse('customer-detail', kwargs={'pk': customer_pk})
        response = client.get(customer_detail_url)
        assert response.status_code == status.HTTP_200_OK

    def test_fetch_all(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects
        """
        client = self.api_client
        response = client.get(reverse('customer-list'))
        assert response.status_code == status.HTTP_200_OK
        assert Customer.objects.count() == len(response.data)

    def test_delete(self):
        """
        Create 3 objects, do a fetch all call and check if you get back 3 objects.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        client = self.api_client
        customer_qs = Customer.objects.all()
        customer_count = Customer.objects.count()

        for i, customer in enumerate(customer_qs, start=1):
            response = client.delete(reverse('customer-detail', kwargs={'pk': customer.pk}))
            assert response.status_code == status.HTTP_204_NO_CONTENT
            assert customer_count - i == Customer.objects.count()

    def test_update_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        client = self.api_client
        customer_pk = Customer.objects.first().pk
        customer_detail_url = reverse('customer-detail', kwargs={'pk': customer_pk})
        customer_dict = factory.build(dict, FACTORY_CLASS=CustomerFactory)
        response = client.patch(customer_detail_url, data=customer_dict)
        assert response.status_code == status.HTTP_200_OK

        assert customer_dict['email'] == response.data['email']

    def test_update_email_with_incorrect_value_outside_constraints(self):
        client = self.api_client
        customer = Customer.objects.first()
        customer_detail_url = reverse('customer-detail', kwargs={'pk': customer.pk})
        customer_email = customer.email
        data = {
            'email': faker.pystr(min_chars=256, max_chars=256),
        }
        response = client.patch(customer_detail_url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert customer_email == Customer.objects.first().email
