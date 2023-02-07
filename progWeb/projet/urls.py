from django.urls import path
from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription' ),
    path('annotation/<int:pk>/', views.annotation, name='annotation'),
    path('annot/', views.Annot.as_view(), name='annot'),
    path('r1/<str:requete>/', views.r1, name='r1'),
    path('r2/', views.R2.as_view(), name='r2'),
]
 