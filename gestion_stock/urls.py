
from django.contrib import admin
from django.urls import path , include
from django.contrib.auth import views as auth_views
from produits import views as produit_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produits.urls')),
    path('register/', produit_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
