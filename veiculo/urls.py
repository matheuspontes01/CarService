from django.urls import path
from veiculo.views import *

urlpatterns = [
    path('', ListarVeiculos.as_view(), name='listar-veiculos'),
    path('novo/', CriarVeiculos.as_view(), name="criar-veiculo"),
    path('editar/<int:pk>/', EditarVeiculos.as_view(), name="editar-veiculo"),
    path('fotos/<str:arquivo>', FotoVeiculo.as_view(), name="foto-veiculo")
]