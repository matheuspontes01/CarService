from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from veiculo.forms import FormularioVeiculo
from veiculo.models import Veiculo

# Create your views here.
class ListarVeiculos(LoginRequiredMixin, ListView):
    # view para listar veículos cadastrados
    model = Veiculo
    context_object_name = 'veiculos'
    template_name = 'listar.html'

    def get_queryset(self, **kwargs):
        pesquisa = self.request.GET.get('pesquisa')
        queryset = Veiculo.objects.all()
        if pesquisa is not None:
            queryset = queryset.filter(modelo__icontains=pesquisa)
        return queryset
    
class CriarVeiculos(LoginRequiredMixin, CreateView):
    # view para criar um novo veículo
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'novo.html'
    success_url = reverse_lazy('listar-veiculos')

class EditarVeiculos(LoginRequiredMixin, UpdateView):
    # view para editar um veículo existente
    model = Veiculo
    form_class = FormularioVeiculo
    template_name = 'editar.html'
    success_url = reverse_lazy('listar-veiculos')

class FotoVeiculo(View):
    # view para exibir a foto do veículo
    def get(self, request, arquivo):
        try:
            veiculo = Veiculo.objects.get(foto='veiculo/fotos/{}'.format(arquivo))
            return FileResponse(veiculo.foto)
        except ObjectDoesNotExist:
            raise Http404("Foto não encontrada ou acesso não autorizado.")
        except Exception as exception:
            raise exception
        
class DeletarVeiculos(LoginRequiredMixin, DeleteView):
    # view para deletar um veículo existente
    model = Veiculo
    template_name = "deletar.html"
    success_url = reverse_lazy('listar-veiculos')