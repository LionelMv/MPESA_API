from django.urls import path
from . import views

urlpatterns = [
    path('get_access_token/', views.get_access_token, name='get_access_token'),
]
