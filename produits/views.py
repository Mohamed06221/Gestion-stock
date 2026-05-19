from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import ProduitForm, CategorieForm, EntreeStockForm, SortiStockForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.core.paginator import Paginator

@login_required
def liste_produit(request):
    recherche = request.GET.get('q', '')
    if recherche:
        produits = Produit.objects.filter(nom__icontains=recherche)
    else:
        produits = Produit.objects.all()
    paginator = Paginator(produits, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'produits/liste.html', {
        'produits': page_obj,
        'page_obj': page_obj,
        'recherche': recherche
    })

@login_required
def ajouter_produit(request):
    if not request.user.is_staff:
        raise PermissionDenied
    form = ProduitForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('liste_produit')
    return render(request, 'produits/formulaire.html', {'form': form})

@login_required
def modifier_produit(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    produit = get_object_or_404(Produit, id=id)
    form = ProduitForm(request.POST or None, instance=produit)
    if form.is_valid():
        form.save()
        return redirect('liste_produit')
    return render(request, 'produits/formulaire.html', {'form': form})

@login_required
def supprimer_produit(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    produit = get_object_or_404(Produit, id=id)
    if request.method == "POST":
        produit.delete()
        return redirect('liste_produit')
    return render(request, 'produits/confirmer_suppression.html', {'produit': produit})

@login_required
def liste_categorie(request):
    recherche = request.GET.get('q', '')
    if recherche:
        categories = Categorie.objects.filter(nom__icontains=recherche)
    else:
        categories = Categorie.objects.all()
    paginator = Paginator(categories, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'produits/categories.html', {
        'categories': page_obj,
        'page_obj': page_obj,
        'recherche': recherche
    })

@login_required
def ajouter_categorie(request):
    if not request.user.is_staff:
        raise PermissionDenied
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categorie')
    else:
        form = CategorieForm()
    return render(request, 'produits/ajouter_categorie.html', {'form': form})

@login_required
def modifier_categorie(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('liste_categorie')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'produits/modifier_categorie.html', {'form': form})

@login_required
def supprimer_categorie(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    categorie = get_object_or_404(Categorie, id=id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categorie')
    return render(request, 'produits/supprimer_categorie.html', {'categorie': categorie})

@login_required
def liste_entrees(request):
    recherche = request.GET.get('q', '')
    entrees = EntreeStock.objects.select_related('produit')
    if recherche:
        entrees = entrees.filter(produit__nom__icontains=recherche)
    entrees = entrees.order_by('-date')
    paginator = Paginator(entrees, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'produits/liste_entrees.html', {
        'entrees': page_obj,
        'page_obj': page_obj,
        'recherche': recherche
    })

@login_required
def ajouter_entree(request):
    if request.method == 'POST':
        form = EntreeStockForm(request.POST)
        if form.is_valid():
            entree = form.save()
            entree.produit.quantite += entree.quantite
            entree.produit.save()
            return redirect('liste_entrees')
    else:
        form = EntreeStockForm()
    return render(request, 'produits/ajouter_entree.html', {'form': form})

@login_required
def liste_sorti(request):
    recherche = request.GET.get('q', '')
    sortis = SortiStock.objects.all()
    if recherche:
        sortis = sortis.filter(produit__nom__icontains=recherche)
    sortis = sortis.order_by('-date')
    paginator = Paginator(sortis, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'produits/liste_sorti.html', {
        'sortis': page_obj,
        'page_obj': page_obj,
        'recherche': recherche
    })

@login_required
def ajouter_sorti(request):
    if request.method == 'POST':
        form = SortiStockForm(request.POST)
        if form.is_valid():
            sorti = form.save(commit=False) # commit=False pour vérifier le stock est disponible avant de sauvegarder
            if sorti.quantite > sorti.produit.quantite:
                form.add_error('quantite', f'Stock insuffisant ! Stock actuel : {sorti.produit.quantite} unités.')
                return render(request, 'produits/ajouter_sorti.html', {'form': form})
            sorti.save()
            sorti.produit.quantite -= sorti.quantite
            sorti.produit.save()
            return redirect('liste_sorti')
    else:
        form = SortiStockForm()
    return render(request, 'produits/ajouter_sorti.html', {'form': form})

@login_required
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def liste_utilisateurs(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    recherche = request.GET.get('q', '')
    if recherche:
        utilisateurs = User.objects.filter(username__icontains=recherche)
    else:
        utilisateurs = User.objects.all()
    paginator = Paginator(utilisateurs, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'produits/liste_utilisateurs.html', {
        'utilisateurs': page_obj,
        'page_obj': page_obj,
        'recherche': recherche
    })

@login_required
def ajouter_utilisateur(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_utilisateurs')
    else:
        form = UserCreationForm()
    return render(request, 'produits/ajouter_utilisateur.html', {'form': form})

@login_required
def supprimer_utilisateur(request, id):
    if not request.user.is_superuser:  
        raise PermissionDenied 
    utilisateur = get_object_or_404(User, id=id)
    if request.method == 'POST': 
        utilisateur.delete()
        return redirect('liste_utilisateurs')
    return render(request, 'produits/supprimer_utilisateur.html', {'utilisateur': utilisateur})

@login_required
def toggle_admin(request, id):
    if not request.user.is_superuser:
        raise PermissionDenied
    utilisateur = get_object_or_404(User, id=id)
    if request.method == 'POST':
        if utilisateur.is_superuser:
            return redirect('liste_utilisateurs')
        utilisateur.is_staff = not utilisateur.is_staff
        utilisateur.save()
        return redirect('liste_utilisateurs')