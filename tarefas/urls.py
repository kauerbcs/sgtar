from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('adicionar/', views.adicionar_tarefa, name='adicionar_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),
]