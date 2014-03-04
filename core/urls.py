from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
    url(r'^problem/(?P<slug>.*)/$', 'problem', name='problem'),
    url(r'^subscribe/$', 'subscribe', name='subscribe'),
    url(r'^confirm/$', 'confirm_email', name='confirm_email'),
    url(r'^update_subscription/$', 'update_subscription', name='update_subscription'),
    url(r'^suggest/$', 'suggest', name='suggest'),
    url(r'^past/$', 'past_problems', name='past_problems'),
)