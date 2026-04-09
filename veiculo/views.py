from django.shortcuts import render
from django.views.generic import ListView

from veiculo.models import Veiculo

# Create your views here.
class ListarVeiculos(ListView):
    # view para listar veículos cadastrados
    model = Veiculo
    context_object_name = 'veiculos'
    template_name = 'listar.html'