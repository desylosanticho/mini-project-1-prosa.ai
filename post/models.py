from django.db import models
from django.conf import settings
from django.urls import reverse

#post models, with account and comment relation
class Post(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='date created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='date updated')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post:post-detail', args=[str(self.id)])