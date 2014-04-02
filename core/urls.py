from django.conf.urls import patterns, url
from core.feeds import rss_feed, atom_feed

urlpatterns = patterns('core.views',
    url(r'^$', 'home', name='home'),
    url(r'^problem/(?P<slug>.*)/$', 'problem', name='problem'),
    url(r'^subscribe/$', 'subscribe', name='subscribe'),
    url(r'^confirm/$', 'confirm_email', name='confirm_email'),
    url(r'^update_subscription/$', 'update_subscription', name='update_subscription'),
    url(r'^suggest/$', 'suggest', name='suggest'),
    url(r'^past/$', 'past_problems', name='past_problems'),
    url(r'^preview/$', 'preview', name='preview'),
)

urlpatterns += patterns('',
    url(r'^rss/$', rss_feed()),
    url(r'^atom/$', atom_feed()),
)