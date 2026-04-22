from django.forms import ModelForm
from veiculo.models import Veiculo

class FormularioVeiculo(ModelForm):
    # formulário para criar um novo veículo
    class Meta:
        model = Veiculo
        exclude = []