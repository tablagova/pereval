from django.urls import path
from .views import PerevalAPIView
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('submitData/', PerevalAPIView.as_view({'post': 'post', 'get': 'get_user_records'})),
    path('submitData/<int:pk>', PerevalAPIView.as_view({'patch': 'edit_one_record', 'get': 'get_one'})),
]

