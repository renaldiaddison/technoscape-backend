from django.urls import path
from . import views

urlpatterns = [
    path('accept/', views.create_loan_view),
    path('approval/', views.create_loan_approval_view),
    path('approval/approve', views.approve_loan_approval_view),
    path('get/', views.get_loan_view), 
    path('pay/', views.pay_loan_view), 
]
