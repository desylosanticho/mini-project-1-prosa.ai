from django.urls import path
from knox import views as knox_views
from . import views

urlpatterns = [
    path('users/', views.get_user),
    path('login/', views.login),
    path('register/', views.register),
    path('', views.UserListRegistration.as_view(), name='user-account'),
    path('profile/<int:id>/', views.UserProfile.as_view(), name='user-profile'),
    path('edit/<int:id>/', views.UserEdit.as_view(), name='user-edit'),
#    path('post-profile/', views.put_profils),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
#    path('profile/', views.ProfileListView  )
] 