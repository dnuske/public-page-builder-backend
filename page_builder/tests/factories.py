from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from page_builder.models import Page, Path

faker = Factory.create()

class PathFactory(DjangoModelFactory):
    class Meta:
        model = Path

    customer = factory.SubFactory('page_builder.tests.factories.CustomerFactory')
    page = factory.SubFactory('page_builder.tests.factories.PageFactory')
    path = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    json_content = LazyAttribute(lambda o: faker.text(max_nb_chars=65535))


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    email = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class CustomerWithForeignFactory(CustomerFactory):
    @factory.post_generation
    def paths(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                PathFactory(customer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                PathFactory(customer=obj)

    @factory.post_generation
    def pages(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                PageFactory(customer=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                PageFactory(customer=obj)


class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    customer = factory.SubFactory('page_builder.tests.factories.CustomerFactory')
    main_url = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    cloudflare_domain = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
    configuration = LazyAttribute(lambda o: faker.text(max_nb_chars=65535))
    github_repo = LazyAttribute(lambda o: faker.text(max_nb_chars=255))


class PageWithForeignFactory(PageFactory):
    @factory.post_generation
    def paths(obj, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for n in range(extracted):
                PathFactory(page_id=obj)
        else:
            number_of_units = randint(1, 10)
            for n in range(number_of_units):
                PathFactory(page_id=obj)
