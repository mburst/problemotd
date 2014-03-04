from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'problemotd.views.home', name='home'),
    url(r'^', include('core.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
