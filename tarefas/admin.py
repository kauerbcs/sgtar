from django.contrib import admin
from .models import Tarefa, Categoria, Tag

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'owner', 'prioridade', 'concluida', 'created_at', 'completed_at', 'categoria')
    list_filter = ('concluida', 'prioridade', 'categoria', 'created_at', 'owner')
    search_fields = ('titulo', 'descricao', 'owner__username')
    list_editable = ('concluida', 'prioridade')
    autocomplete_fields = ('categoria',)
    filter_horizontal = ('tags',)  # ou use raw_id_fields se preferir

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ('nome',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ('nome',)