from django.urls import path
from store import views

urlpatterns = [
    path('', views.HomeListView.as_view(), name='index'),
    path('product/<slug>/', views.ProductDetailsView.as_view(), name='product-details')
]