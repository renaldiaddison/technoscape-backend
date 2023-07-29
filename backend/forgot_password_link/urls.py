from django.urls import path
from . import views

urlpatterns = [
    path('generate/', views.generate_forgot_password_link_api_view),
    path('validate/', views.validate_forgot_password_link_api_view),
]
