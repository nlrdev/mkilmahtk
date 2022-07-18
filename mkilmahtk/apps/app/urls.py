from django.urls import path
from .views import (
    app,
    registration,
    login,
    logout,
    
)

urlpatterns = [
    path("registration/", registration, name="registration"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("", app, name="app"),
    path("<slug:page>/", app, name="app"),
    path("<slug:page>/<slug:function>/", app, name="app"),
]
