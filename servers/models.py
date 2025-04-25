from random import randint
import ipaddress
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.exceptions import ValidationError

from django.contrib.auth import get_user_model
User = get_user_model()


class Status(models.TextChoices):
    PENDING = 'PEN', 'Pending'
    ACTIVE = 'ACT', 'Active'
    APPROVED = 'APP', 'Approved'
    REJECTED = 'REJ', 'Rejected'
    DELETED = 'DEL', 'Deleted'


class OperatingSystem(models.Model):
    name = models.CharField(max_length=200)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    patch_level = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.major_version}.{self.minor_version}.{self.patch_level}'


class Network(models.Model):
    vlan_name = models.CharField(max_length=100)
    ipv4_address = models.GenericIPAddressField(protocol='IPv4')
    netmask = models.GenericIPAddressField(protocol='IPv4', default='255.255.255.0')

    def __str__(self):
        return f'{self.vlan_name} - {self.ipv4_address}/{self.netmask}'

    def get_next_free_ip(self, network):
        net = ipaddress.ip_network(f'{self.ipv4_address}/{self.netmask}', strict=False)
        allocated_ips = (ipaddress.ip_address(server.primary_ip_address) for server in Server.objects.all())
        hosts = list(net.hosts())
        for ip in hosts[1:len(hosts)-1]:
            if ip not in allocated_ips:
                return str(ip)
        return None


class Domain(models.Model):
    name = models.CharField(max_length=200)
    ns1 = models.CharField(max_length=200)
    ns2 = models.CharField(max_length=200)

    def __str__(self):
        return str(self.name)


class Group(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Server(models.Model):
    name = models.CharField(
        max_length=200, blank=True,
        help_text="""Der Hostname wird automatisch generiert, wenn keiner vergeben wird.""")
    domain = models.ForeignKey(Domain, related_name='servers', on_delete=models.DO_NOTHING, null=True, blank=True)
    primary_ip_address = models.GenericIPAddressField(
        protocol='IPv4', unique=True, null=True, blank=True,
        #validators=[Network.validate_ip],
        help_text="""Es wird die nächste freie IP aus dem zugewisesenen Netz automatisch zugewiesen.""")
    network = models.ForeignKey(Network, related_name='servers', on_delete=models.CASCADE)
    cpu = models.IntegerField(validators=[MaxValueValidator(16)], null=True, blank=True, help_text="Cores")
    memory = models.IntegerField(validators=[MaxValueValidator(65536)],  null=True, blank=True, help_text="RAM GB")
    disk = models.IntegerField(validators=[MaxValueValidator(65536)],  null=True, blank=True, help_text="Disk GB")
    vendor = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(choices=Status.choices, default=Status.PENDING, max_length=3)
    groups = models.ManyToManyField(Group, related_name='servers')
    os = models.ForeignKey(OperatingSystem, related_name='servers', on_delete=models.CASCADE)
    meta_data = models.JSONField(blank=True, null=True)
    extra_data = models.JSONField(blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='servers', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.__generate_hostname()
        if not self.primary_ip_address:  # Nur setzen, wenn keine IP-Adresse angegeben ist
            next_ip = self.network.get_next_free_ip(self.network)
            if next_ip:
                self.primary_ip_address = next_ip
            else:
                raise ValidationError("Keine freien IP-Adressen im Netzwerk verfügbar.")
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        self.status = Status.DELETED
        self.save()

    def __generate_hostname(self):
        return f"srv{randint(0,9999999):08d}"

    def __str__(self):
        return str(self.name)


class NetworkInterface(models.Model):
    server = models.ForeignKey(
        Server,
        on_delete=models.CASCADE,
        related_name='interfaces'
    )
    ipv4 = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True)
    mac = models.CharField(max_length=17, blank=True)
    vendor = models.CharField(max_length=100, blank=True)
    TYPE_CHOICES = (
        ('lan', 'LAN'),
        ('wifi', 'WiFi'),
        ('dmz', 'DMZ'),
        ('mgm', 'Management'),
        ('svc', 'Service'),
        ('n/c', 'Not Connected')
    )
    type = models.CharField(max_length=4, choices=TYPE_CHOICES, default='lan')
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name} ({self.type})"
