from django.urls import path

from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.Acceuil.as_view(), name='acceuil'),
]
