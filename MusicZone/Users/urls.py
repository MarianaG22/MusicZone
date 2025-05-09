from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
   path('usuarios/', views.user, name='user'),
   path('crear/', views.add_user, name='add_user'),
   path('editar/<int:usuario_id>/', views.edit_user, name='edit_user'),
   path('eliminar/<int:usuario_id>/', views.remove_user, name='remove_user'),

   path('roles/add/', views.add_role, name='add_role'),
   path('roles/edit/int:role_id/', views.edit_role, name='edit_role'),
   path('roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),

]