# eventos/forms.py
from django import forms
from .models import Torneio, Inscricao, ResultadoJogo

class TorneioForm(forms.ModelForm):
    class Meta:
        model = Torneio
        fields = ['nome', 'data', 'hora', 'tipo_torneio']

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['jogador']

class ResultadoJogoForm(forms.ModelForm):
    class Meta:
        model = ResultadoJogo
        fields = ['set1', 'set2', 'set3', 'set4', 'set5', 'pontuacao']
