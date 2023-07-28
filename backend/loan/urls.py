from django.urls import path
from . import views

urlpatterns = [
    path('approval/', views.create_loan_approval_view),
    path('approval/approve', views.approve_loan_approval_view),
]
