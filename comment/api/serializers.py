from rest_framework import serializers
from comment.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username', read_only=True)
    post = serializers.ReadOnlyField(source='post.pk', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'owner', 'post', 'updated_at']