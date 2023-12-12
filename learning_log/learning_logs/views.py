from django.shortcuts import render
from .forms import TopicForm
from .models import Topic
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TopicForm


def index(request):
    """Página principal do site Learning_log"""
    return render(request, 'learning_logs/index.html')

def topics(request):
    """mostra todos os assuntos buscando do banco"""
    topic = Topic.objects.order_by('date_added')
    contex = {'topics': topic}
    return render(request,'learning_logs/topics.html', contex)

def topic(request, topic_id):
    """mostra um unico assunto e suas entradas"""
    topic =Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context ={'topic': topic, 'entries': entries}
    return render(request,'learning_logs/topic.html', context)

from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TopicForm

def new_topic(request):
    """Adiciona um novo tópico"""
    if request.method != 'POST':
        # Nenhum dado submetido; cria um formulário em branco
        form = TopicForm()
    else:
        # Dados de POST submetidos; processar os dados
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}   
    return render(request, 'learning_logs/new_topic.html', context)
