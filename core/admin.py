from django.contrib import admin
from django.db.models import get_models, get_app

#Registers all models to admin interface http://djangosnippets.org/snippets/2066/
for model in get_models(get_app('core')):
    try:
        admin.site.register(model)
    except:
        pass
