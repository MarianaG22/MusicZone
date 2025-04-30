from django.contrib import admin
from .models import Sale, Sale_Detail, Order, Cart, Cart_Item

# Register your models here.
admin.site.register(Sale)
admin.site.register(Sale_Detail)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Cart_Item)