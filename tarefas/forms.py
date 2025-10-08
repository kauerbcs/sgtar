from django import forms
from .models import Tarefa, Categoria, Tag

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'concluida', 'prioridade', 'categoria', 'tags']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 4}),
            'concluida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'prioridade': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select', 'size': 5}),
        }

    def clean_titulo(self):
        titulo = (self.cleaned_data.get('titulo') or '').strip()
        if not titulo:
            raise forms.ValidationError("O título é obrigatório.")
        if len(titulo) < 3:
            raise forms.ValidationError("O título precisa ter pelo menos 3 caracteres.")
        return titulo