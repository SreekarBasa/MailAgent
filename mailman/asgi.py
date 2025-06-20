# asgi.py
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailman.settings')

import django
django.setup()

from django.core.asgi import get_asgi_application
from fastapi_routes import fastapi_app
from starlette.applications import Starlette
from starlette.routing import Mount

# Initialize Django ASGI application
django_app = get_asgi_application()

# Combine Django and FastAPI routes
# Mount FastAPI at /api/ and Django at /
app = Starlette(
    routes=[
        Mount('/api', app=fastapi_app),
        Mount('/', app=django_app),
    ]
)