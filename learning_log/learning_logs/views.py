from django.shortcuts import render
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def index(request):
    """Página principal do site Learning_log"""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """mostra todos os assuntos buscando do banco"""
    #topic = Topic.objects.order_by('date_added')//código anterior comentado
    # incluindo filtro por dono //código atual a baixo:
    topic = Topic.objects.filter(owner=request.user).order_by('date_added')
    
    context = {'topics': topic}
    return render(request,'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """mostra um unico assunto e suas entradas"""
    topic =Topic.objects.get(id = topic_id)

    #Garantir que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404

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
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('topics'))

    context = {'form': form}   
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    #Garantir que o assunto pertence ao usuário atual
    if topic.owner != request.user:
        raise Http404

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
    try:
        entry = Entry.objects.get(id=entry_id)
    except Entry.DoesNotExist:
        raise Http404("A entrada não existe.")

    # Verifica se o usuário logado é o dono do tópico associado à entrada
    if entry.topic.owner != request.user:
        raise Http404("Você não tem permissão para editar esta entrada.")

    topic = entry.topic

    if request.method != 'POST':
        # Requisição inicial, preenche previamente a entrada do formulário atual
        form = EntryForm(instance=entry)
    else:
        # Dados de Post submetidos, processa os dados
        form = EntryForm(data=request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('topic', args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    # Verifica se o usuário logado é o dono da entrada
    if entry.topic.owner != request.user:
        raise Http404("Você não tem permissão para excluir esta entrada.")

    # Exclui a entrada e redireciona para a página do tópico
    entry.delete()
    return HttpResponseRedirect(reverse('topic', args=[entry.topic.id]))




