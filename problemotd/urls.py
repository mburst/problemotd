from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'problemotd.views.home', name='home'),
    url(r'^', include('core.urls')),
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)
