import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 🔑 oldinga olib qo'ydik

django_asgi_app = get_asgi_application()

# 🔑 routing importini endi settings yuklangandan keyin qildik
from pages.routing import websocket_urlpatterns  

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
