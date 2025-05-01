from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalog, name='catalog')
]