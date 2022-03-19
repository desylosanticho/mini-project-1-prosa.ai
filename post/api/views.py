from post.models import Post
from post.api.serializers import PostSerializer
from post.permission import IsOwnerOrReadOnly

from account.renderers import MyRenderer

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics


class PostList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    renderer_classes = [MyRenderer]
    queryset = Post.objects.all().order_by("id")

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    renderer_classes = [MyRenderer]
    queryset = Post.objects.all()
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)