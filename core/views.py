import platform
import sys
import socket
from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Deployment


def get_client_ip(request):
    """Extract client IP from request, handling proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_db_replica_status():
    """Check PostgreSQL replication status."""
    try:
        with connection.cursor() as cursor:
            # Check if we're in recovery mode (replica)
            cursor.execute("SELECT pg_is_in_recovery();")
            in_recovery = cursor.fetchone()[0]

            if in_recovery:
                # Get replication lag
                cursor.execute("""
                    SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp())) 
                    AS lag_seconds;
                """)
                lag = cursor.fetchone()[0] or 0
                return f"replica (lag: {lag:.2f}s)"
            else:
                # Check replication connections
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_replication;
                """)
                replicas = cursor.fetchone()[0]
                if replicas > 0:
                    return f"primary ({replicas} replica(s))"
                return "primary (standalone)"
    except Exception as e:
        return f"error: {str(e)}"


def index(request):
    """Main dashboard view showing all deployments and system info."""
    deployments = Deployment.objects.all()[:50]

    # Gather system information
    context = {
        'deployments': deployments,
        'system_info': {
            'hostname': socket.gethostname(),
            'server_ip': socket.getaddrinfo(socket.gethostname(), None)[0][4][0],
            'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            'django_version': __import__('django').get_version(),
            'platform': platform.platform(),
            'processor': platform.processor() or 'N/A',
            'db_host': settings.DATABASES['default']['HOST'],
            'db_name': settings.DATABASES['default']['NAME'],
            'db_replica_status': get_db_replica_status(),
            'client_ip': get_client_ip(request),
            'nginx_port': request.META.get('SERVER_PORT', '4443'),
            'handled_by': socket.gethostname(),
        },
        'total_deployments': Deployment.objects.count(),
        'environments': dict(Deployment.ENVIRONMENT_CHOICES),
    }
    return render(request, 'core/index.html', context)


def deployment_detail(request, pk):
    """Detail view for a specific deployment record."""
    deployment = get_object_or_404(Deployment, pk=pk)
    return render(request, 'core/detail.html', {'deployment': deployment})


@csrf_exempt
@require_http_methods(["POST"])
def api_create_deployment(request):
    """API endpoint to create a new deployment record."""
    try:
        import json
        data = json.loads(request.body)

        deployment = Deployment.objects.create(
            hostname=data.get('hostname', socket.gethostname()),
            server_ip=data.get('server_ip', '127.0.0.1'),
            deployment_environment=data.get('deployment_environment', 'development'),
            nginx_port=data.get('nginx_port', 4443),
            gunicorn_workers=data.get('gunicorn_workers', 4),
            gunicorn_port=data.get('gunicorn_port', 8000),
            node_role=data.get('node_role', 'primary'),
            os_version=data.get('os_version', platform.release()),
            python_version=data.get('python_version', platform.python_version()),
            django_version=data.get('django_version', __import__('django').get_version()),
            db_host=data.get('db_host', settings.DATABASES['default']['HOST']),
            db_replica_status=data.get('db_replica_status', 'unknown'),
            request_source_ip=get_client_ip(request),
            handled_by=socket.gethostname(),
        )

        return JsonResponse({
            'success': True,
            'id': deployment.id,
            'message': 'Deployment record created successfully'
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)


def api_health(request):
    """Health check endpoint for load balancer monitoring."""
    try:
        # Test database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()

        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    return JsonResponse({
        'status': 'healthy' if db_status == 'healthy' else 'degraded',
        'database': db_status,
        'hostname': socket.gethostname(),
        'timestamp': datetime.now().isoformat(),
    })


def api_deployments(request):
    """API endpoint to list all deployments as JSON."""
    deployments = Deployment.objects.all().values()
    return JsonResponse({
        'count': len(deployments),
        'deployments': list(deployments)
    })
