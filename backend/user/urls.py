from django.urls import path

from . import views

urlpatterns = [
    path('auth/create/', views.create_user_api_view),
    path('auth/login/', views.login_user_api_view),
    path('info/', views.get_user_api_view),
    path('bank-account/', views.get_user_bank_account_view),
]
