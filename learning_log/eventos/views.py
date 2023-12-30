# eventos/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Torneio, Inscricao, ResultadoJogo
from .forms import TorneioForm, InscricaoForm, ResultadoJogoForm


@login_required
def criar_torneio(request):
    if request.method == 'POST':
        form = TorneioForm(request.POST)
        if form.is_valid():
            torneio = form.save()
            return redirect('eventos:detalhes_torneio', torneio_id=torneio.id)
    else:
        form = TorneioForm()
    return render(request, 'eventos/criar_torneio.html', {'form': form})

@login_required
def detalhes_torneio(request, torneio_id):
    torneio = get_object_or_404(Torneio, pk=torneio_id)
    inscricoes = Inscricao.objects.filter(torneio=torneio)
    return render(request, 'eventos/detalhes_torneio.html', {'torneio': torneio, 'inscricoes': inscricoes})

@login_required
def adicionar_jogador(request, torneio_id):
    torneio = get_object_or_404(Torneio, pk=torneio_id)
    if request.method == 'POST':
        form = InscricaoForm(request.POST)
        if form.is_valid():
            inscricao = form.save(commit=False)
            inscricao.torneio = torneio
            inscricao.save()
            return redirect('eventos:detalhes_torneio', torneio_id=torneio.id)

    else:
        form = InscricaoForm()
    return render(request, 'eventos/adicionar_jogador.html', {'form': form, 'torneio': torneio})


@login_required
def adicionar_resultado(request, torneio_id, inscricao_id):
    torneio = get_object_or_404(Torneio, pk=torneio_id)
    inscricao = get_object_or_404(Inscricao, pk=inscricao_id, torneio=torneio)

    if request.method == 'POST':
        form = ResultadoJogoForm(request.POST)
        if form.is_valid():
            resultado = form.save(commit=False)
            resultado.pontuacao = calcular_pontuacao(resultado)  # Adapte esta função conforme necessário
            resultado.save()
            inscricao.resultado_jogo = resultado
            inscricao.save()
            return redirect('eventos:detalhes_torneio', torneio_id=torneio.id)
    else:
        form = ResultadoJogoForm()

    return render(request, 'eventos/adicionar_resultado.html', {'form': form, 'torneio': torneio, 'inscricao': inscricao})


def calcular_pontuacao(resultado):
    # Adapte esta função de acordo com a lógica desejada para calcular a pontuação
    # Exemplo simples: 1 ponto por jogo ganho
    pontos = 0
    if resultado.set1 > resultado.set2:
        pontos += 1
    if resultado.set2 > resultado.set1:
        pontos += 1
    # Adicione lógica para os sets 3, 4 e 5, se necessário
    return pontos

