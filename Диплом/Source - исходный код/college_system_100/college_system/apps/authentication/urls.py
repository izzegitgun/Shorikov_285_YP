from django.urls import path

from . import views

app_name = "authentication"

urlpatterns = [
    path("profile/", views.profile_view, name="profile"),
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_edit"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user_delete"),
]


