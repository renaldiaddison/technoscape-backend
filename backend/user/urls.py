from django.urls import path

from . import views

urlpatterns = [
    path('auth/create/', views.create_user_api_view),
    path('auth/login/', views.login_user_api_view),
    path('forgot-password/', views.forgot_password_api_view),
    path('info/', views.get_user_api_view),
    path('approve/', views.approve_user_api_view),
    path('bank-account/', views.get_user_bank_account_api_view),
    path('transaction/create-transaction/', views.create_transaction_api_view),
    path('verify-pin/', views.verify_pin_api_view),
    path('transaction/info/', views.get_user_transaction_api_view),
    path('transaction/info/transfer-in',
         views.get_user_transaction_transfer_in_api_view),
    path('connected-user-account/',
         views.get_connected_user_account_api_view),

]
