from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('account.api.urls')),
    path('api/posts/', include('post.api.urls', "post"), name="post"),
    path('api/posts/', include('comment.api.urls', "comment"), name="comment"),
    path('api/user/', include("account.api.urls"), name="account")
]