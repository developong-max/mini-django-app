from django.db import models
import socket


class Deployment(models.Model):
    """Stores infrastructure deployment information."""

    ENVIRONMENT_CHOICES = [
        ('development', 'Development'),
        ('staging', 'Staging'),
        ('production', 'Production'),
        ('testing', 'Testing'),
        ('dr', 'Disaster Recovery'),
    ]

    hostname = models.CharField(max_length=255, help_text="Server hostname")
    server_ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, 
                                              help_text="Server IP address")
    deployment_environment = models.CharField(
        max_length=20, 
        choices=ENVIRONMENT_CHOICES,
        default='development',
        help_text="Deployment environment"
    )
    nginx_port = models.PositiveIntegerField(default=4443, help_text="NGINX SSL port")
    time_of_deployment = models.DateTimeField(auto_now_add=True, help_text="Timestamp of deployment")

    # Additional metadata
    gunicorn_workers = models.PositiveIntegerField(default=4, help_text="Number of Gunicorn workers")
    gunicorn_port = models.PositiveIntegerField(default=8000, help_text="Gunicorn bind port")
    node_role = models.CharField(max_length=50, default='primary', help_text="Node role: primary/secondary")
    os_version = models.CharField(max_length=100, blank=True, help_text="FreeBSD version")
    python_version = models.CharField(max_length=50, blank=True, help_text="Python version")
    django_version = models.CharField(max_length=50, blank=True, help_text="Django version")
    db_host = models.CharField(max_length=255, blank=True, help_text="PostgreSQL host")
    db_replica_status = models.CharField(max_length=50, default='unknown', help_text="Replication status")
    request_source_ip = models.GenericIPAddressField(null=True, blank=True, help_text="Client IP")
    handled_by = models.CharField(max_length=255, blank=True, help_text="Which backend handled the request")

    class Meta:
        ordering = ['-time_of_deployment']
        verbose_name = 'Deployment Record'
        verbose_name_plural = 'Deployment Records'

    def __str__(self):
        return f"{self.hostname} ({self.deployment_environment}) - {self.server_ip}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('deployment_detail', kwargs={'pk': self.pk})
