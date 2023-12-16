from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required




def index(request):
    """Página principal do site Learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """mostra todos os assuntos buscando do banco"""
    topic = Topic.objects.order_by('date_added')
    contex = {'topics': topic}
    return render(request,'learning_logs/topics.html', contex)

@login_required
def topic(request, topic_id):
    """mostra um unico assunto e suas entradas"""
    topic =Topic.objects.get(id = topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context ={'topic': topic, 'entries': entries}
    return render(request,'learning_logs/topic.html', context)

@login_required
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

@login_required
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

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)
    
@login_required
def edit_entry(request, entry_id):
    """Edita uma entrada existente"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method !='POST':
        # Requesição inicial, preenche previamente a entrada do formulario atual
        form = EntryForm(instance=entry)

    else:
        # dados de Post submetidos processa os dados
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form} 
    return render(request,'learning_logs/edit_entry.html', context)       