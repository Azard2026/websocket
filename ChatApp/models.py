from django.db import models
from django.utils.timezone import now

# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255)

    def __str__(self):
        return self.room_name
    

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # on delete mean if the room is deleted all msgs are deleted
    sender = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)  # Add a timestamp field
   

    def __str__(self):
        return f"{self.room.room_name} - {self.sender} ({self.timestamp})"
    


class ChatRoom(models.Model):
    user1 = models.CharField(max_length=255)  # Participant 1 (could be an identifier like username or email)
    user2 = models.CharField(max_length=255)  # Participant 2
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Room: {self.user1} & {self.user2}"

class singleMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=255)  # Sender identifier
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender}: {self.message} ({self.timestamp})"
