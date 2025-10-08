from django import forms
from .models import Tarefa

class TarefaForm(forms.ModelForm):
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'concluida']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 4}),
            'concluida': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_titulo(self):
        titulo = (self.cleaned_data.get('titulo') or '').strip()
        if not titulo:
            raise forms.ValidationError("O título é obrigatório.")
        if len(titulo) < 3:
            raise forms.ValidationError("O título precisa ter pelo menos 3 caracteres.")
        # opcional: evitar títulos duplicados (descomente se quiser)
        # if Tarefa.objects.filter(titulo__iexact=titulo).exists():
        #     raise forms.ValidationError("Já existe uma tarefa com este título.")
        return titulo

    def clean_descricao(self):
        descricao = (self.cleaned_data.get('descricao') or '').strip()
        if not descricao:
            raise forms.ValidationError("A descrição é obrigatória.")
        if len(descricao) < 5:
            raise forms.ValidationError("A descrição precisa ter pelo menos 5 caracteres.")
        return descricao