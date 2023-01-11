from django.urls import path

from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.Accueil.as_view(), name='accueil'),
]
