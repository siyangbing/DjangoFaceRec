from django.urls import path

from face_sqlite import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]
