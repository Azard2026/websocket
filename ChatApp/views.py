from django.shortcuts import render,redirect, get_object_or_404
from .models import Room,Message,ChatRoom,singleMessage
import json


from datetime import datetime, timedelta
from django.utils.timezone import now
# Create your views here.
def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST['username']
        room = request.POST['room']
        try:
            get_room = Room.objects.get(room_name=room)
            return redirect('room', room_name=room, username=username)
        except Room.DoesNotExist:
            new_room = Room(room_name=room)
            new_room.save()
            return redirect('room', room_name=room, username=username)
    return render(request, 'index.html')


def MessageView(request, room_name, username):
    get_room = Room.objects.get(room_name=room_name)
    get_messages = Message.objects.filter(room=get_room).order_by('timestamp')

    # Group messages by date
    grouped_messages = {}
    today = now().date()
    yesterday = today - timedelta(days=1)

    for message in get_messages:
        msg_date = message.timestamp.date()
        if msg_date == today:
            date_key = "Today"
        elif msg_date == yesterday:
            date_key = "Yesterday"
        else:
            date_key = msg_date.strftime("%B %d, %Y")  # e.g., "January 18, 2025"

        if date_key not in grouped_messages:
            grouped_messages[date_key] = []
        grouped_messages[date_key].append(message)

    context = {
        "grouped_messages": grouped_messages,
        "user": username,
        "room_name": room_name,
    }
    return render(request, 'message.html', context)

def SingleCreateRoom(request):
    if request.method == 'POST':
        user1 = request.POST.get('username')
        user2 = request.POST.get('user1')

        # Validate input
        if not user1 or not user2:
            return render(request, 'chat-index.html', {'error': 'Both users must be provided.'})

        # Ensure consistent ordering of user identifiers
        sorted_users = sorted([user1, user2])
        room_name = f"room_{sorted_users[0]}_{sorted_users[1]}"

        # Get or create the room
        room, created = ChatRoom.objects.get_or_create(
            user1=sorted_users[0],
            user2=sorted_users[1],
        )

        return redirect('one_to_one_chat',user1=user1,user2=user2)
    return render(request,'chat-index.html')        
        
  

def one_to_one_chat(request, user1, user2):
    # Ensure consistent ordering of user identifiers
    sorted_users = sorted([user1, user2])
    room_name = f"room_{sorted_users[0]}_{sorted_users[1]}"

    # Get or create the room
    room, created = ChatRoom.objects.get_or_create(
        user1=sorted_users[0],
        user2=sorted_users[1],
    )

    # Fetch messages for the room
    messages = singleMessage.objects.filter(room=room).order_by('timestamp')
     # Group messages by date
    grouped_messages = {}
    today = now().date()
    yesterday = today - timedelta(days=1)

    for message in messages:
        msg_date = message.timestamp.date()
        if msg_date == today:
            date_key = "Today"
        elif msg_date == yesterday:
            date_key = "Yesterday"
        else:
            date_key = msg_date.strftime("%B %d, %Y")  # e.g., "January 18, 2025"

        if date_key not in grouped_messages:
            grouped_messages[date_key] = []
        grouped_messages[date_key].append(message)
    # print(grouped_messages)

    return render(request, 'chat.html', {
        'room_name': room_name,
        'user1': user1,
        'user2': user2,
        'grouped_messages': grouped_messages,
    })




def CallView(request, room_name, username):
    # Add proper JSON serialization
    config = {
        'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]
    }
    return render(request, 'call.html', {
        'room_name': room_name,
        'user': username,
        'config': json.dumps(config)  # Serialize to JSON string
    })