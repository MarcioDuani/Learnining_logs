# eventos/models.py
from django.db import models
from django.contrib.auth.models import User

class Torneio(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    hora = models.TimeField()
    tipo_torneio = models.CharField(max_length=50)
    jogadores = models.ManyToManyField(User, through='Inscricao')

class Inscricao(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.CASCADE)
    torneio = models.ForeignKey(Torneio, on_delete=models.CASCADE)
    resultado_jogo = models.ForeignKey('ResultadoJogo', on_delete=models.SET_NULL, null=True, blank=True)

class ResultadoJogo(models.Model):
    set1 = models.PositiveIntegerField()
    set2 = models.PositiveIntegerField()
    set3 = models.PositiveIntegerField(blank=True, null=True)
    set4 = models.PositiveIntegerField(blank=True, null=True)
    set5 = models.PositiveIntegerField(blank=True, null=True)
    pontuacao = models.PositiveIntegerField(default=0)  # Adicionando a pontuação

