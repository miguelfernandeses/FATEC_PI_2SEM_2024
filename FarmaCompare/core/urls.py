from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('escolher_plano/', views.escolher_plano, name='escolher_plano'),
    path('card/', views.card, name='card'),
    path('main/', views.lista_produtos, name='main'),
    path('search/', views.search, name='search'),
    path('conta/', views.conta, name= 'conta' )
]

