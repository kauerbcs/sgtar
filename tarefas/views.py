from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Tarefa, Categoria, Tag
from .forms import TarefaForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registro bem-sucedido. Você está logado.')
            return redirect('index')
        else:
            messages.error(request, 'Corrija os erros no formulário abaixo.')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def index(request):
    # base queryset: superuser vê tudo, outros apenas suas tarefas
    if request.user.is_superuser:
        base_qs = Tarefa.objects.all()
    else:
        base_qs = Tarefa.objects.filter(owner=request.user)

    q = request.GET.get('q', '').strip()
    prioridade = request.GET.get('prioridade', '')
    categoria = request.GET.get('categoria', '')
    status = request.GET.get('status', '')  # 'pendente'|'concluida'|''

    # filtros (aplicados sempre em base_qs)
    if q:
        base_qs = base_qs.filter(Q(titulo__icontains=q) | Q(descricao__icontains=q))

    if prioridade in ('alta', 'media', 'baixa'):
        base_qs = base_qs.filter(prioridade=prioridade)

    if categoria.isdigit():
        base_qs = base_qs.filter(categoria__id=int(categoria))

    if status == 'concluida':
        base_qs = base_qs.filter(concluida=True)
    elif status == 'pendente':
        base_qs = base_qs.filter(concluida=False)

    # contagens agregadas (uma única query)
    counts = base_qs.aggregate(
        total=Count('id'),
        concluidas=Count('id', filter=Q(concluida=True)),
        pendentes=Count('id', filter=Q(concluida=False)),
        alta_prioridade=Count('id', filter=Q(prioridade='alta')),
    )

    # otimizações: prefetch/select_related antes da paginação
    qs = (
        base_qs
        .select_related('categoria', 'owner')  # FK
        .prefetch_related('tags')              # M2M
        .order_by('-id')
    )

    # paginação configurável (padrão 10)
    per_page = getattr(settings, 'TAREFAS_PER_PAGE', 10)
    paginator = Paginator(qs, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categorias = Categoria.objects.all()
    tags = Tag.objects.all()

    context = {
        'tarefas': page_obj.object_list,   # compatibilidade com template (lista exibida)
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        # contagens agregadas
        'total_count': counts['total'],
        'tarefas_concluidas_count': counts['concluidas'],
        'tarefas_pendentes_count': counts['pendentes'],
        'tarefas_alta_prioridade_count': counts['alta_prioridade'],
        'q': q,
        'prioridade_selected': prioridade,
        'categoria_selected': categoria,
        'status_selected': status,
        'categorias': categorias,
        'tags': tags,
    }
    return render(request, 'tarefas/index.html', context)

@require_http_methods(["GET", "POST"])
@login_required
def adicionar_tarefa(request):
    if request.method == 'POST':
        form = TarefaForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tarefa = form.save(commit=False)
                    tarefa.owner = request.user
                    tarefa.save()
                    form.save_m2m()
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
@login_required
def editar_tarefa(request, tarefa_id):
    if request.user.is_superuser:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id)
    else:
        tarefa = get_object_or_404(Tarefa, id=tarefa_id, owner=request.user)

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
@login_required
def excluir_tarefa(request, tarefa_id):
    try:
        if request.user.is_superuser:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id)
        else:
            tarefa = get_object_or_404(Tarefa, id=tarefa_id, owner=request.user)

        tarefa.delete()
        messages.success(request, 'Tarefa excluída com sucesso.')
    except Exception as e:
        messages.error(request, f'Erro ao excluir a tarefa: {e}')
    return redirect('index')