from django.db import models
from django.conf import settings

class Appointment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE)
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='lawyer_appointments', on_delete=models.CASCADE)
    date = models.DateTimeField()
    notes = models.TextField(blank=True)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user} → {self.lawyer} @ {self.date}"
    
    def get_conversation(self):
        """Get the conversation associated with this appointment"""
        try:
            return Conversation.objects.get(user=self.user, lawyer=self.lawyer)
        except Conversation.DoesNotExist:
            return None


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_user', on_delete=models.CASCADE)
    lawyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conversations_as_lawyer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lawyer')

    def __str__(self):
        return f"Conversation: {self.user} <> {self.lawyer}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Msg by {self.sender} at {self.created_at}"


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='notifications_received', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    conversation = models.ForeignKey(Conversation, null=True, blank=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification to {self.recipient}: {self.message[:30]}..."
