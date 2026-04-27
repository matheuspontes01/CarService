from django.urls import path
from anuncio.views import *

urlpatterns = [
    path('', ListarAnuncios.as_view(), name='listar-anuncios'),
    path('novo/', CriarAnuncios.as_view(), name='criar-anuncio'),
    path('editar/<int:pk>/', EditarAnuncios.as_view(), name='editar-anuncio')
]