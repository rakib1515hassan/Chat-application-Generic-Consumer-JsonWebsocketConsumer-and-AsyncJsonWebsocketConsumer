import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import ChatApp.routing

# For Authentication
from channels.auth import AuthMiddlewareStack  


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,

    'websocket': AuthMiddlewareStack(
        URLRouter(
            ChatApp.routing.websocket_urlpatterns
            )
        ),

    ## NOTE Without authentication--------------------

    # 'websocket': URLRouter(
    #     ChatApp.routing.websocket_urlpatterns
    #     )

})

