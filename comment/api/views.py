from cgitb import lookup
from comment.models import Comment
from post.models import Post
from django.shortcuts import get_object_or_404
from comment.api.serializers import CommentSerializer
from rest_framework import generics

from account.renderers import MyRenderer
from post.permission import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination


class CommentList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    renderer_classes = [MyRenderer]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user, post=self.get_object())

    def get_queryset(self):
        return self.queryset.filter(post=self.kwargs["post_id"])

    def get_object(self):
        obj = get_object_or_404(Post, pk=self.kwargs["post_id"])
        return obj


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    renderer_classes = [MyRenderer]
    queryset = Comment.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        post_id = self.kwargs["post_id"]
        comment_id = self.kwargs["id"]
        return self.queryset.filter(post=post_id, id=comment_id)
