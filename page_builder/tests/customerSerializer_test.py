from datetime import datetime

import factory
from django.test import TestCase
from django.urls import reverse
from rest_framework import serializers
from rest_framework.test import APIRequestFactory

from page_builder.serializers import CustomerSerializer

from .factories import (
    CustomerFactory,
    CustomerWithForeignFactory,
    PageFactory,
    PathFactory,
)


class CustomerSerializer_Test(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.customer = CustomerWithForeignFactory.create()

    def test_that_a_customer_is_correctly_serialized(self):
        customer = self.customer
        serializer = CustomerSerializer
        serialized_customer = serializer(customer).data

        assert serialized_customer['id'] == customer.id
        assert serialized_customer['email'] == customer.email

        assert len(serialized_customer['paths']) == customer.paths.count()

        assert len(serialized_customer['pages']) == customer.pages.count()
