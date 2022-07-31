from django.urls import path
from order import views

app_name = 'store'
urlpatterns = [
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add-to-cart'),
    path('view-cart/', views.cart_view, name='view-cart'),
    path('remove-item/<int:pk>/', views.remove_item_from_cart, name='remove-item'),
]