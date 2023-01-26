from django.urls import path
from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.Accueil.as_view(), name='accueil'),
    path('connexion/', views.Connexion.as_view(), name='connexion'),
    path('inscription/', views.Inscription.as_view(), name='inscription' ),
    path('inscription/createuser', views.Inscription.create_user, name='inscription2' ),
    path('annotation/', views.Annotation.as_view(), name='annotation'),
    path('thanks/', views.Thanks.as_view(), name='thanks'),
]
 