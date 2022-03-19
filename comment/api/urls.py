from django.urls import path

from . import views

app_name = "comment"
urlpatterns = [
    path("<int:post_id>/comments/", views.CommentList.as_view(), name="comment-list"),
    path(
        "<int:post_id>/comments/<int:id>/",
        views.CommentDetail.as_view(),
        name="comment-detail",
    ),
]
