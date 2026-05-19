from django import forms
from .models import Produit , Categorie , EntreeStock , SortiStock

class ProduitForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom', 'categorie', 'prix', 'quantite']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Nom du produit'
            }),
            'categorie': forms.Select(attrs={
                'class': 'select w-full',  # ← Select pas TextInput
            }),
            'prix': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Prix'
            }),
            'quantite': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Quantite'
            }),
        }
    

class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Nom de la catégorie'
            })
        }

class EntreeStockForm(forms.ModelForm):
    class Meta:
        model = EntreeStock
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={
                'class': 'select w-full',
            }),
            'quantite': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Quantité'
            })
        }

class SortiStockForm(forms.ModelForm):
    class Meta:
        model = SortiStock
        fields = ['produit', 'quantite']
        widgets = {
            'produit': forms.Select(attrs={
                'class': 'select w-full',
            }),
            'quantite': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Quantité'
            })
        }