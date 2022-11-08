from django.contrib import admin
from django.apps import apps
#Registers all models to admin interface https://stackoverflow.com/a/30064494/1907292
app = apps.get_app_config('core')

for model_name, model in app.models.items():
    admin.site.register(model)
