from django.conf import settings
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)

    def __str__(self):
        return self.nome

class Tag(models.Model):
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    PRIORIDADE_ALTA = 'alta'
    PRIORIDADE_MEDIA = 'media'
    PRIORIDADE_BAIXA = 'baixa'
    PRIORIDADES = [
        (PRIORIDADE_ALTA, 'Alta'),
        (PRIORIDADE_MEDIA, 'Média'),
        (PRIORIDADE_BAIXA, 'Baixa'),
    ]

    titulo = models.CharField(max_length=200, verbose_name='Título')
    descricao = models.TextField(verbose_name='Descrição')
    concluida = models.BooleanField(default=False, verbose_name='Concluída')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Concluído em')
    prioridade = models.CharField(max_length=10, choices=PRIORIDADES, default=PRIORIDADE_MEDIA, verbose_name='Prioridade')
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL, related_name='tarefas', verbose_name='Categoria')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tarefas', verbose_name='Tags')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tarefas', verbose_name='Proprietário')


    def save(self, *args, **kwargs):
        if self.concluida and not self.completed_at:
            self.completed_at = timezone.now()
        if not self.concluida and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo