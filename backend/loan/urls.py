from django.urls import path
from . import views

urlpatterns = [
    path('accept/', views.create_loan_view),
    path('approval/', views.create_loan_approval_view),
    path('approval/approve/', views.approve_loan_approval_view),
    path('approval/unapprove/', views.unapprove_loan_approval_view),
    path('get/', views.get_loan_view), 
    path('pay/', views.pay_loan_view),
    path('history/', views.get_loan_history_view),
    path('approval/get/', views.get_all_approval_view),
    # path('admin/approval/', views.admin_view_approvals),
    # path('admin/', views.admin_view_loans), 
]
