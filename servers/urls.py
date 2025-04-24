from django.urls import path
from .views import server_list_view, scan_network

urlpatterns = [
    path('', server_list_view, name='server_list'),
    path('scan/', scan_network, name='scan_network'),
]
