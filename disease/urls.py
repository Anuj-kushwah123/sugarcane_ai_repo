from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='home'),
    path('predict/', views.predict_disease_view, name='predict_disease'),
]