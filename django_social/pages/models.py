from django.db import models
from django.utils import timezone


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField('tags.Tag', null=True, blank=True, related_name='pages')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='pages')
    followers = models.ManyToManyField('users.User', null=True, blank=True, related_name='follows')
    image = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField('users.User', null=True, blank=True, related_name='requests')
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.uuid

    def block(self, end_date=None):
        self.is_blocked = True
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
