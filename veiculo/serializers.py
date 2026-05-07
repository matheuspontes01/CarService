from rest_framework.serializers import ModelSerializer, SerializerMethodField
from veiculo.models import Veiculo

class SerializadorVeiculo(ModelSerializer):
    """Serializador para o modelo Veiculo, utilizado para 
    converter os dados do modelo em formatos como JSON ou XML, 
    facilitando a comunicação entre a aplicação e outras
    partes do sistema, como APIs ou interfaces de usuário."""
    nome_marca = SerializerMethodField()
    nome_cor = SerializerMethodField()
    nome_combustivel = SerializerMethodField()

    class Meta:
        model = Veiculo
        exclude = ['marca', 'cor', 'combustivel']

    def get_nome_marca(self, instancia):
        return instancia.get_marca_display()

    def get_nome_cor(self, instancia):
        return instancia.get_cor_display()

    def get_nome_combustivel(self, instancia):
        return instancia.get_combustivel_display()