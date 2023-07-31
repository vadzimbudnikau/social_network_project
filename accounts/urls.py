from django.urls import path
from . import views

"""
URL Configuration for the 'accounts' app.

This module defines URL patterns for the 'accounts' app. It maps URLs to the corresponding view functions
to handle user authentication, profile display, and profile editing.

Attributes:
    app_name (str): The namespace for URL patterns of the 'accounts' app.
    urlpatterns (list): The list of URL patterns for the 'accounts' app.
"""
app_name = 'accounts'

urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('accounts/profile/<slug:slug>/', views.ProfileDetailView.as_view(), name='profile'),
    path('accounts/profile/<slug:slug>/edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('accounts/profile/<slug:slug>/followers', views.FollowersListView.as_view(), name='followers'),
    path('accounts/profile/<slug:slug>/following', views.FollowingListView.as_view(), name='following'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/profile/<slug:slug>/password_change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('<slug:slug>/follow/', views.FollowView.as_view(), name='follow'),
    path('<slug:slug>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),
]
