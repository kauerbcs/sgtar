from django.contrib import admin
from .models import Tarefa

# Register your models here.
admin.site.site_header = "Administração do SGTAR"
admin.site.site_title = "SGTAR Admin"
admin.site.index_title = "Painel de Administração do SGTAR"

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'descricao', 'concluida')  # colunas que aparecem na lista
    list_filter = ('concluida',)  # filtro lateral
    search_fields = ('titulo', 'descricao')  # barra de busca
    list_editable = ('concluida',)  # permite marcar como concluída direto na lista
