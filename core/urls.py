from django.urls import path, re_path

from core import views
from core.feeds import atom_feed, rss_feed

urlpatterns = [
    path("", views.home, name="home"),
    re_path(r"^problem/(?P<slug>.*)/$", views.problem, name="problem"),
    path("subscribe/", views.subscribe, name="subscribe"),
    path("confirm/", views.confirm_email, name="confirm_email"),
    path("update_subscription/", views.update_subscription, name="update_subscription"),
    path("suggest/", views.suggest, name="suggest"),
    path("past/", views.past_problems, name="past_problems"),
    path("preview/", views.preview, name="preview"),
    re_path(
        r"^delete/(?P<comment_id>.*)/$", views.delete_comment, name="delete_comment"
    ),
    path("login/", views.login, name="login"),
    path("rss/", rss_feed()),
    path("atom/", atom_feed()),
]
