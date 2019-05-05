from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^sign-up/$',
        views.signing_up,
        name='signing_up'),
    url(r'^sign-in/$',
        auth_views.LoginView.as_view(template_name="authproj/sign_in.html"),
        name='signing_in'),
    url(r'^sign-out/$',
        auth_views.LogoutView.as_view(),{"next_page": "/"},
        name='signing_out'),
]