from django.urls import path
from . import views

app_name = 'projet'
urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('connexion/', views.connexion, name='connexion'),
    path('inscription/', views.inscription, name='inscription' ),
    path('annotation/', views.Annotation.as_view(), name='annotation'),
    path('annot/', views.Annot.as_view(), name='annot'),
    path('r1/<str:requete>/', views.r1, name='r1'),
    path('r2/<str:requete>/', views.r2, name='r2'),
]