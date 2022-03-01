from django.contrib import admin
from django.contrib import messages
from django.contrib.auth import get_user_model
from authemail.admin import EmailUserAdmin

from .models import Page, Path
from page_builder.actions import *

class CustomerAdmin(EmailUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 
                                       'is_superuser', 'is_verified', 
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom info', {'fields': ('date_of_birth',)}),
    )
    
@admin.action(description='Trigger page deployment')
def trigger_page_deploy(modeladmin, request, queryset):
    for page in queryset:
        try:
            trigger_page_deploy(page)
            messages.add_message(request, messages.INFO, "Se creó el deployment")
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.message)


@admin.action(description='Create Cloudflare page')
def create_cloudflare_page(modeladmin, request, queryset):
    for page in queryset:
        try:
            create_cloudflare_page(page)
            messages.add_message(request, messages.INFO, "Pagina creada en Cloud Flare")
        except RepositoryNotFoundError:
            messages.add_message(request, messages.ERROR,
                               "Repositorio en GitHub no definido. Establezca el repositorio a usar primero")
            return
        except Exception as e:
            messages.add_message(request, messages.ERROR, e.message)
            return


@admin.action(description='Create GitHub repository')
def create_github_repository(modeladmin, request, queryset):
    for page in queryset:
        try:
            create_github_repository(page)

        except RepositoryAlreadyExistsError:
            messages.add_message(request, messages.ERROR, "Ya existe un repoitorio asignado")
        except GithubRepositoryCreationError as e:
            messages.add_message(request, messages.ERROR, "\n".join(e.json['errors']))
        except HTTPError as http_err:
            messages.add_message(request, messages.ERROR, f'HTTP error: {http_err}')
        except Exception as err:
            messages.add_message(request, messages.ERROR, f"Hubo un error al establecer la petición HTTP: {err}")

@admin.action(description='Push changes to GH repo')
def push_to_repo(modeladmin, request, queryset):
    for page in queryset:
        try:
            print("start push_to_repository")
            push_to_repository(page)
            print("end push_to_repository")
        except Exception as e:
            messages.add_message(request, messages.ERROR, str(e))



class PageAdmin(admin.ModelAdmin):
    actions=[create_github_repository, create_cloudflare_page, trigger_page_deploy, push_to_repo]

admin.site.register(Page, PageAdmin)
admin.site.register(Path)

admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), CustomerAdmin)



