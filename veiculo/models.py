from django.db import models
from veiculo.consts import *
from datetime import datetime

# Create your models here.
class Veiculo(models.Model):
    marca = models.SmallIntegerField(choices=OPCOES_MARCAS)
    modelo = models.CharField(max_length=100)
    ano = models.IntegerField()
    cor = models.SmallIntegerField(choices=OPCOES_CORES)
    combustivel = models.SmallIntegerField(choices=OPCOES_COMBUSTIVEIS)
    foto = models.ImageField(blank=True, null=True, upload_to='veiculo/fotos')

    def __str__(self):
        return f'{self.get_marca_display()} {self.modelo} ({self.ano})'

    def anos_de_uso(self):
        return datetime.now().year - self.ano

    # Propriedade para verificar se o veículo é novo (ano atual) -> Não se torna informação armazenada no banco, mas sim uma propriedade calculada dinamicamente
    @property
    def veiculo_novo(self):
        return self.ano == datetime.now().year