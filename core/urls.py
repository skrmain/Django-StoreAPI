from django.urls import path

from core import views

urlpatterns = [
    path('me/', views.UserView.as_view()),
    path('products/', views.ProductView.as_view()),
    path('products/<int:product_id>/save/', views.ProductSaveView.as_view()),
    path('saved/', views.SavedView.as_view()),
    path('cart/', views.CartView.as_view()),
    path('cart/products/<int:product_id>/', views.CartProductView.as_view()),
]
