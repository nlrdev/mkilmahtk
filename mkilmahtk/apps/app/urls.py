from django.urls import path
from .views import (
    app,
)
from accounts.views import (
    registration,
    login,
    logout,
)

urlpatterns = [
    # accounts urls
    path("registration/", registration, name="registration"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    # app urls
    path("", app, name="app"),
    path("<slug:page>/", app, name="app"),
    path("<slug:page>/<slug:function>/", app, name="app"),
]
