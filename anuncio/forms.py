from django.forms import ModelForm
from anuncio.models import Anuncio

class FormularioAnuncio(ModelForm):
    # formulário para criar um novo anúncio
    class Meta:
        model = Anuncio
        exclude = ['usuario']