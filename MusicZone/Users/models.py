from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=100, verbose_name='Rol')

    def __str__(self):
        return self.role

class User(AbstractUser):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    last_name = models.CharField(max_length=100, verbose_name='Apellido')
    username = models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')
    email = models.EmailField(unique=True, verbose_name='Correo electrónico')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name='Rol', null=True, blank=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    def __str__(self):
        return self.username