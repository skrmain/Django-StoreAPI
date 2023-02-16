from django.urls import path

from core import views

urlpatterns = [
    path('me/', views.UserDetailView.as_view()),
]
