from django.urls import path
from . import views

urlpatterns = [
    path('predict/', views.model_predict_api_view)
]
