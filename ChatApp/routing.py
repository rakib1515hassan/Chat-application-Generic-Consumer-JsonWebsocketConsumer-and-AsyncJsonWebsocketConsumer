from django.urls import path
from ChatApp import consumers


websocket_urlpatterns = [
    path('ws/jwc/<str:group_name>/', consumers.MyJsonWebsocketConsumer.as_asgi()),
    # path('ws/jwc/', consumers.MyJsonWebsocketConsumer.as_asgi()),

    path('ws/ajwc/<str:group_name>/', consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
    # path('ws/ajwc/', consumers.MyAsyncJsonWebsocketConsumer.as_asgi()),
]