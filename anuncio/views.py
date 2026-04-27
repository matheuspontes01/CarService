from django.shortcuts import render
from django.urls import reverse_lazy

from anuncio.models import Anuncio
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from anuncio.forms import FormularioAnuncio

# Create your views here.
class ListarAnuncios(LoginRequiredMixin, ListView):
    # view para listar veículos cadastrados
    model = Anuncio
    context_object_name = 'anuncios'
    template_name = 'listaranuncios.html'

    def get_queryset(self, **kwargs):
        pesquisa = self.request.GET.get('titulo')
        queryset = Anuncio.objects.all()
        if pesquisa is not None:
            queryset = queryset.filter(titulo__icontains=pesquisa)
        return queryset

class CriarAnuncios(LoginRequiredMixin, CreateView):
    # view para criar um novo anuncio
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'novoanuncio.html'
    success_url = reverse_lazy('listar-anuncios')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class EditarAnuncios(LoginRequiredMixin, UpdateView):
    #view para editar um anuncio existente
    model = Anuncio
    form_class = FormularioAnuncio
    template_name = 'editaranuncio.html'
    success_url = reverse_lazy('listar-anuncios')