from django.urls import path
from .views import server_list_view

urlpatterns = [
    path('', server_list_view, name='server_list'),
]

