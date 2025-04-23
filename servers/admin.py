
from unfold.admin import ModelAdmin
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.forms import ValidationError as FormValidationError
from .models import Server, NetworkInterface, Network, Status, OperatingSystem, Domain, Group


admin.site.site_header = "ClickOps"
admin.site.site_title = "Administration"
admin.site.index_title = "DFR IT AG"


class NetworkInterfaceInline(admin.TabularInline):
    model = NetworkInterface
    extra = 1


@admin.register(Server)
class ServerAdmin(ModelAdmin):
    list_display = ('name', 'domain', 'primary_ip_address', 'cpu', 'memory', 'disk', 'status', 'os')
    search_fields = ('name',)
    list_filter = ('domain', 'os','status', 'groups',)

    actions = ['activate_servers', 'deactivate_servers', 'delete_selected_servers']

    inlines = [NetworkInterfaceInline]
    
    @admin.action(description='Activate selected servers')
    def activate_servers(self, request, queryset):
        queryset.update(status=Status.ACTIVE)
        self.message_user(request, "Selected servers were activated.")

    def save_model(self, request, obj, form, change):
        try:
            obj.save()
        except ValidationError as e:
            form.add_error(None, FormValidationError(e.message))
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:server_id>/undelete/', self.admin_site.admin_view(self.undelete_view), name='server-undelete'),
            path('<int:server_id>/deploy/', self.admin_site.admin_view(self.deploy_view), name='server-deploy'),
        ]
        return custom_urls + urls

    def undelete_view(self, request, server_id):
        server = self.get_object(request, server_id)
        # Implementiere hier die Undelete-Logik
        server.is_deleted = False
        server.save()
        messages.success(request, f'Server {server.hostname} wurde wiederhergestellt.')
        return redirect('admin:myapp_server_change', server_id)

    def deploy_view(self, request, server_id):
        server = self.get_object(request, server_id)
        # Implementiere hier die Deploy-Logik
        messages.success(request, f'Server {server.hostname} wurde erfolgreich deployed.')
        return redirect('admin:myapp_server_change', server_id)


@admin.register(Network)
class NetworkAdmin(ModelAdmin):
    list_display = ('vlan_name', 'ipv4_address', 'netmask')

@admin.register(Domain)
class DomainAdmin(ModelAdmin):
    list_display = ('name', 'ns1', 'ns2')

@admin.register(Group)
class GroupAdmin(ModelAdmin):
    list_display = ('name',)

@admin.register(OperatingSystem)
class OperatingSystemAdmin(ModelAdmin):
    list_display = ('name', 'major_version', 'minor_version', 'patch_level')

