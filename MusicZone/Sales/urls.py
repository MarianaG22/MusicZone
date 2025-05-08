from django.urls import path
from . import views

urlpatterns = [
    # Carrito
    path("carrito/", views.cart_view, name="cart_view"),
    path("cart/add/<int:instrument_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path('cart/increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    
    path("register-sale/", views.register_sale, name="register_sale"),
    path("ordenes/", views.order_list, name="order_list"),
    path('ordenes/toggle-status/<int:order_id>/', views.toggle_order_status, name='toggle_order_status'),
]
