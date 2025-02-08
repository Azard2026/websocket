from django.urls import path
from . import views


urlpatterns = [
    path('', views.CreateRoom, name='create-room'),

    path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
    path('call/<str:room_name>/<str:username>/', views.CallView, name='call_room'),
    path('one_to_one_chat/',views.SingleCreateRoom,name='singleCreateroom'),
    path('one_to_one_chat/<str:user1>/<str:user2>/', views.one_to_one_chat, name='one_to_one_chat'),

]