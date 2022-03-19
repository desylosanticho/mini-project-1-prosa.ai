from django.db import models
from django.conf import settings
from post.models import Post

class Comment(models.Model):
    body = models.TextField(max_length=1000, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='date created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='date updated')

    def __str__(self):
        return self.body[:10]