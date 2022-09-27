from django.contrib import admin
from django.apps import apps
from django.contrib.auth.models import Group
# Register your models here.

models = apps.get_models()

admin.site.unregister(Group)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        # admin.site.unregister(model)
        pass
