from django.shortcuts import render, redirect
from tarefas.models import Tarefa

# Create your views here.
def index(request):
    tarefas = Tarefa.objects.all()
    return render(request, 'tarefas/index.html', {'tarefas': tarefas})

def adicionar_tarefa(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        Tarefa.objects.create(titulo=titulo, descricao=descricao)
        return redirect('index')
    return render(request, 'tarefas/adicionar_tarefa.html')

def editar_tarefa(request, tarefa_id):
    tarefa = Tarefa.objects.get(id=tarefa_id)
    if request.method == 'POST':
        tarefa.titulo = request.POST.get('titulo')
        tarefa.descricao = request.POST.get('descricao')
        tarefa.concluida = 'concluida' in request.POST
        tarefa.save()
        return redirect('index')
    return render(request, 'tarefas/editar_tarefa.html', {'tarefa': tarefa})

def excluir_tarefa(request, tarefa_id):
    tarefa = Tarefa.objects.get(id=tarefa_id)
    tarefa.delete()
    return redirect('index')