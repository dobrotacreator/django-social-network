from django.db import models


class Post(models.Model):
    page = models.ForeignKey('pages.Page', on_delete=models.CASCADE, related_name='posts')
    content = models.CharField(max_length=180)
    liked_by = models.ManyToManyField('users.User', related_name='liked_posts')
    reply_to = models.ForeignKey('posts.Post', on_delete=models.SET_NULL, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
