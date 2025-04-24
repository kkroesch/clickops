from django.shortcuts import render

from rest_framework import viewsets
from .models import Network, Server
from .serializers import NetworkSerializer, ServerSerializer
from django.views.decorators.http import require_http_methods
import nmap, json

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
                'type': iface.type
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


@require_http_methods(["GET", "POST"])
def scan_network(request):
    result = None
    network_selected = None
    auto_import = request.POST.get("auto_import") == "on"

    if request.method == "POST":
        network_id = request.POST.get("network")
        network_selected = Network.objects.get(id=network_id)
        net_range = network_selected.ipv4_address  # z. B. "192.168.1.0/24"
        nm = nmap.PortScanner()
        nm.scan(hosts=net_range, arguments='-O -p 22,9090')

        result = []
        for ip in nm.all_hosts():
            h = nm[ip]
            mac = h['addresses'].get('mac')
            data = {
                "ip": ip,
                "hostname": h.hostname(),
                "mac": mac,
                "vendor": h['vendor'].get(mac, '') if 'vendor' in h else '',
                "os": h['osmatch'][0]['name'] if h.get('osmatch') else None,
                "ports": {
                    "22": h['tcp'][22]['state'] if 22 in h.get('tcp', {}) else "closed",
                    "9090": h['tcp'][9090]['state'] if 9090 in h.get('tcp', {}) else "closed"
                }
            }
            result.append(data)

            # Import bei gesetzter Checkbox
            if auto_import and mac and not Server.objects.filter(primary_ip_address=ip).exists():
                existing = Server.objects.filter(network=network_selected, primary_ip_address__isnull=False, primary_ip_address=ip)
                if not existing.exists():
                    Server.objects.get_or_create(
                        network=network_selected,
                        primary_ip_address=ip,
                        defaults={
                            'name': h.hostname() or ip.replace('.', '-'),
                            'cpu': 1,
                            'memory': 512,
                            'disk': 16,
                            'status': 'PND',
                        }
                    )

    return render(request, "servers/scan.html", {
        "networks": Network.objects.all(),
        "result": json.dumps(result, indent=2) if result else None,
        "network_selected": network_selected,
        "auto_import": auto_import,
    })
