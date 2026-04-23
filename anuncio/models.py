from django.db import models
from django.utils import timezone
from veiculo.models import Veiculo
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField


# Create your models here.
class Anuncio(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_criacao = models.DateTimeField(default=timezone.now)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


