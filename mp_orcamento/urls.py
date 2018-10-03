from django.urls import path
from .views import *

urlpatterns = [
    path('orcamentos/', orcamentos_lista, name='orcamentos-lista'),
    path('orcamentos/estatisticas/', orcamentos_estatisticas, name='orcamentos-estatisticas'),

    path('clientes/estatisticas/', clientes_estatisticas, name='clientes-estatisticas'),
    path('clientes/<int:id_cliente>/', dados_cliente, name='dados-clientes'),
]
