from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import Tarefa
from .forms import TarefaForm

def index(request):
    tarefas = Tarefa.objects.all().order_by('-id')  # opcional: mais recentes primeiro
    return render(request, 'tarefas/index.html', {'tarefas': tarefas})

@require_http_methods(["GET", "POST"])
def adicionar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Tarefa adicionada com sucesso.')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao salvar a tarefa: {e}')
        else:
            messages.error(request, 'Corrija os erros no formulário abaixo.')
    else:
        form = TarefaForm()
    return render(request, 'tarefas/adicionar_tarefa.html', {'form': form})

@require_http_methods(["GET", "POST"])
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                messages.success(request, 'Tarefa atualizada com sucesso.')
                return redirect('index')
            except Exception as e:
                messages.error(request, f'Não foi possível atualizar a tarefa: {e}')
        else:
            messages.error(request, 'Corrija os erros no formulário abaixo.')
    else:
        form = TarefaForm(instance=tarefa)
    return render(request, 'tarefas/editar_tarefa.html', {'form': form, 'tarefa': tarefa})

@require_http_methods(["POST"])
def excluir_tarefa(request, tarefa_id):
    # excluímos apenas via POST — mais seguro
    try:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        tarefa.delete()
        messages.success(request, 'Tarefa excluída com sucesso.')
    except Exception as e:
        messages.error(request, f'Erro ao excluir a tarefa: {e}')
    return redirect('index')