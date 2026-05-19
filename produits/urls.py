from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('',views.liste_produit, name= "liste_produit"),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'), 
    path('modifier/<int:id>/', views.modifier_produit, name='modifier_produit'), 
    path('supprimer/<int:id>/', views.supprimer_produit, name='supprimer_produit'), 
    path('categories/', views.liste_categorie, name='liste_categorie'),
    path('categories/ajouter/', views.ajouter_categorie, name='ajouter_categorie'),
    path('categories/modifier/<int:id>/', views.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:id>/', views.supprimer_categorie, name='supprimer_categorie'),
    path('entrees/', views.liste_entrees, name='liste_entrees'),
    path('entrees/ajouter/', views.ajouter_entree, name='ajouter_entree'),
    path('sorti/', views.liste_sorti, name='liste_sorti'),
    path('sorti/ajouter/', views.ajouter_sorti, name='ajouter_sorti'),
    path('utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('utilisateurs/ajouter/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('utilisateurs/supprimer/<int:id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('utilisateurs/toggle/<int:id>/', views.toggle_admin, name='toggle_admin'),
]