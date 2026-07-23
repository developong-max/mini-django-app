from django.contrib import admin
from .models import Deployment


@admin.register(Deployment)
class DeploymentAdmin(admin.ModelAdmin):
    list_display = [
        'hostname', 'server_ip', 'deployment_environment', 
        'nginx_port', 'time_of_deployment', 'node_role', 'db_replica_status'
    ]
    list_filter = ['deployment_environment', 'node_role', 'db_replica_status', 'time_of_deployment']
    search_fields = ['hostname', 'server_ip', 'os_version']
    readonly_fields = ['time_of_deployment', 'request_source_ip', 'handled_by']
    date_hierarchy = 'time_of_deployment'

    fieldsets = (
        ('Core Information', {
            'fields': ('hostname', 'server_ip', 'deployment_environment', 'nginx_port')
        }),
        ('Application Stack', {
            'fields': ('gunicorn_workers', 'gunicorn_port', 'node_role')
        }),
        ('System Information', {
            'fields': ('os_version', 'python_version', 'django_version')
        }),
        ('Database', {
            'fields': ('db_host', 'db_replica_status')
        }),
        ('Request Metadata', {
            'fields': ('request_source_ip', 'handled_by', 'time_of_deployment'),
            'classes': ('collapse',)
        }),
    )
