from django.contrib import messages
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from authemail.models import EmailUserManager, EmailAbstractUser
from page_builder.custom_types import PageStatusCodes

class Customer(EmailAbstractUser):
    # Custom fields
    date_of_birth = models.DateField('Date of birth', null=True, blank=True)

    # Required
    objects = EmailUserManager()


class Page(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    main_url = models.CharField(max_length=255, null=True, blank=True)
    cloudflare_domain = models.CharField(max_length=255, null=True, blank=True)
    cloudflare_project_name = models.CharField(max_length=255, null=True, blank=True)
    configuration = models.CharField(max_length=65535, null=True, blank=True)
    github_repo = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='pages')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    status_code = models.IntegerField(null=False, default=PageStatusCodes.INITIAL.value)
    status_message = models.CharField(max_length=65535, null=True, blank=True)
    deploy_status = models.CharField(max_length=255, null=True, blank=True)
    deploy_date_started = models.DateTimeField(null=True, blank=True)
    deploy_date_ended = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.name.replace(" ", "-")
        self.name = self.name.lower()
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "page"
        unique_together = ['user', 'name']


class Path(models.Model):

    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=255)
    json_content = models.CharField(max_length=65535, null=True, blank=True)
    user = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='paths')
    page = models.ForeignKey('Page', on_delete=models.CASCADE, related_name='paths')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.path)

    class Meta:
        db_table = "path"
        unique_together = ['page', 'path']
