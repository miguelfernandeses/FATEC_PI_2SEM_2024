from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.auth_view, name='auth'),
    path('logout/', views.logout_view, name='logout'),
    path('selecionar-plano/', views.selecionar_plano, name='selecionar_plano'),
    path('card/', views.card, name='card'),
    path('main/', views.lista_produtos, name='main'),
    path('search/', views.search, name='search'),
    path('produto/<str:name>/<str:nome_farmacia>/', views.produto_detalhes, name='produto_detalhes'),
    path('produtos/<str:ean>/<str:nome_farmacia>/', views.produtos_detalhe, name='produtos_detalhes'),
    path('busca/', views.busca, name='busca'), 
] 

