from django.shortcuts import render

from rest_framework import viewsets
from .models import Network, Server
from .serializers import NetworkSerializer, ServerSerializer
import subprocess


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = Network.objects.all()
    serializer_class = NetworkSerializer


class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer


def ping(ip):
    try:
        subprocess.check_output(['ping', '-c', '1', '-W', '1', ip], stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False


def server_list_view(request):
    servers = Server.objects.select_related('domain', 'os').prefetch_related('interfaces').all().order_by('domain__name')

    server_data = []
    for server in servers:
        interfaces = []
        for iface in server.interfaces.all():
            ip = iface.ipv4
            reachable = True #ping(str(ip))
            interfaces.append({
                'name': iface.name,
                'ip': ip,
                'reachable': reachable,
            })

        server_data.append({
            'id': server.id,
            'domain': f"{server.name}.{server.domain.name}" if server.domain else server.name,
            'cpu': f"{server.cpu} cores",
            'memory': f"{server.memory} MB",
            'disk': f"{server.disk} GB",
            'os': server.os.name,
            'status': server.get_status_display(),
            'interfaces': interfaces,
        })

    return render(request, 'servers/list.html', {'servers': server_data})
