from django.shortcuts import render
from .models import Topic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TopicForm, EntryForm


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


def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = EntryForm()
    else:
        # POST data submitted, Process Data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.owner = request.user
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('topic',args=[topic_id] ))
    # Display a blank or invalid form
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


