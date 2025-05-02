from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_auth, name='login'),
    path('login_auth/', views.login_auth, name='login_auth'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_auth, name='register'),
]