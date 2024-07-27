# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # path('login/', views.login_view, name='login'),
    path("user/", views.UserList.as_view(), name="user-list"),
]