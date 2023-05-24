from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(unique=True)
    image = models.URLField(null=True, blank=True)
    role = models.CharField(max_length=9, choices=Roles.choices)
    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    def block(self, end_date=None):
        self.is_blocked = True
        for page in self.pages:
            page.block(end_date)
        if end_date:
            self.blocked_until = end_date
        self.save()

    def unblock(self):
        self.is_blocked = False
        self.blocked_until = None
        self.save()

    @property
    def is_blocked_now(self):
        if self.is_blocked and self.blocked_until and self.blocked_until > timezone.now():
            return True
        self.unblock()
        return False
