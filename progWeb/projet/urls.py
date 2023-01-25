from django.urls import path
from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.Accueil.as_view(), name='accueil'),
    path('connexion/', views.Connexion.as_view(), name='connexion'),
    path('inscription/', views.Inscription.as_view(), name='inscription'),
    path('annotation/', views.Annotation.as_view(), name='annotation'),
]
