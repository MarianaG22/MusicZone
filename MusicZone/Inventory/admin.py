from django.contrib import admin
from .models import Type, Mark, Instrument

# Register your models here.
admin.site.register(Type)
admin.site.register(Mark)
admin.site.register(Instrument)