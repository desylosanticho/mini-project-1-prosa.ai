from rest_framework import serializers
from post.models import Post
from django.conf import settings
from comment.models import Comment


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username", read_only=True)
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["id", "title", "body", "owner", "comments", "updated_at"]
 