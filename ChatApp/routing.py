from django.urls import path,re_path
from .consumers import ChatConsumer,OneToOneChatConsumer,CallConsumer,CallConsumergroup

websocket_urlpatterns = [
    path('ws/notification/<str:room_name>/', ChatConsumer.as_asgi()),
     path('ws/one_to_one_chat/<str:user1>/<str:user2>/', OneToOneChatConsumer.as_asgi()),
      path('ws/call/<str:room_name>/', CallConsumer.as_asgi()),
      re_path(r'ws/call/(?P<room_name>\w+)/$',CallConsumergroup.as_asgi()),
      
]