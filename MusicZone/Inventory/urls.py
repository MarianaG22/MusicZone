from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('instrumento/', views.instrumento, name='instrumento'),
    path('crear/', views.crear_instrumento, name='crear_instrumento'),
    path('instrumento/eliminar/<int:instrument_id>/', views.eliminar_instrumento, name='eliminar_instrumento'),
    path('instrumento/editar/<int:instrument_id>/', views.editar_instrumento, name='editar_instrumento'),

    path('catalogo/', views.catalog, name='catalog'),
]