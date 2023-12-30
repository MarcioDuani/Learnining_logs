# eventos/urls.py
from django.urls import path
from .views import criar_torneio, detalhes_torneio, adicionar_jogador, adicionar_resultado

app_name = 'eventos'

urlpatterns = [
    path('criar_torneio/', criar_torneio, name='criar_torneio'),
    path('<int:torneio_id>/', detalhes_torneio, name='detalhes_torneio'),
    path('<int:torneio_id>/adicionar_jogador/', adicionar_jogador, name='adicionar_jogador'),
    path('<int:torneio_id>/<int:inscricao_id>/adicionar_resultado/', adicionar_resultado, name='adicionar_resultado'),
]
