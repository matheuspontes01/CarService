from django.urls import path
from veiculo.views import *

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculos.as_view(), name="criar-veiculo"),
    path('editar/<int:pk>/', EditarVeiculos.as_view(), name="editar-veiculo"),
    path('deletar/<int:pk>/', DeletarVeiculos.as_view(), name="deletar-veiculo"),
    path('api/listar/', APIListarVeiculos.as_view(), name="api-listar-veiculos"),
    path('api/deletar/<int:pk>/', APIDeletarVeiculos.as_view(), name="api-deletar-veiculo"),
    path('api/editar/<int:pk>/', APIDetalharAtualizarVeiculo.as_view(), name="api-editar-veiculo"),
    path('fotos/<str:arquivo>', FotoVeiculo.as_view(), name="foto-veiculo")
] 