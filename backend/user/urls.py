from django.urls import path

from . import views

urlpatterns = [
    path('auth/create', views.create_user_api_view),
]
