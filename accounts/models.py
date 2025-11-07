from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('lawyer', 'Lawyer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    # Optional profile fields
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True)
    cases_fought = models.PositiveIntegerField(default=0)
    cases_won = models.PositiveIntegerField(default=0)
    fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.username} ({self.role})"