from django.db import models
from django.utils.timezone import now

class Email(models.Model):
    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    uid = models.CharField(max_length=255, unique=True)
    sender = models.CharField(max_length=255)
    subject = models.TextField()
    body = models.TextField()
    date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} ({self.priority})"
