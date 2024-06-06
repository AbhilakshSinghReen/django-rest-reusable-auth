from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from core.models.managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True, max_length=255, blank=False)
    full_name = models.CharField(max_length=255, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email


class UserInvite(models.Model):
    QUEUED = 'queued'
    SENT = 'sent'
    USER_CREATED = 'user_created'
    
    STATUS_CHOICES = [
        (QUEUED, 'Invite Queued'),
        (SENT, 'Sent'),
        (USER_CREATED, 'User Created'),
    ]

    email = models.EmailField(unique=True, max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    senders_name = models.CharField(max_length=255, blank=False)
    invite_sent_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=QUEUED)
    resend_invite = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User Invite'
        verbose_name_plural = 'User Invites'
    
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if CustomUser.objects.filter(email=self.email).exists():
            raise ValidationError("A user with this email has already been registered.")
        
        super().save(*args, **kwargs)
