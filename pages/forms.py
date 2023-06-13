from django import forms
from .models import Page


class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'description', 'textoExtraMail','con_mail_personalizado', 'asunto_mail', 'cuerpo_mail' , 'dia', 'horaDesde', 'horaHasta', 'flyer', 'cupo',
                  'modalidad', 'categories', 'provincia','con_preinscripcion', 'secreta', 'clave' , 'responsable', 'colaborador']
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'textoExtraMail': forms.Textarea(attrs={'class': 'form-control'}),
            'dia': forms.Select(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Dia'}),
            'horaDesde': forms.TimeInput(format="%H:%M", attrs={'type': 'time', 'required': True}),
            'horaHasta': forms.TimeInput(format="%H:%M", attrs={'type': 'time', 'required': True}),
            'flyer': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Flyer'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'modalidad': forms.CheckboxInput(attrs={'class': 'form-control check', 'placeholder': 'Es Online?'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control', 'placeholder': 'Categorias'}),
            'responsable': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Responsable'}),
            'colaborador': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Colaborador'}),
            'provincia': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Provincia'}),
            'con_preinscripcion': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Es con preinscripcion?', 'initial': 0, 'default': 0}),
            'secreta': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Es secreta?', 'initial': 0, 'default': 0}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'con_mail_personalizado': forms.CheckboxInput(attrs={'class': 'form-control', 'placeholder': 'Es con mail personalizado?', 'initial': 0, 'default': 0}),
            'asunto_mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mail'}),
            'cuerpo_mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cuerpo del mail'}),
        }
        labels = {'title': '', 'description': ''}

    def __init__(self, *args, **kwargs):
        if kwargs['instance'] is not None:
            if kwargs['instance'].modalidad is None:
                kwargs['initial'] = {"modalidad": False}
            if kwargs['instance'].secreta is None:
                kwargs['initial']['secreta'] = False
        else:
            kwargs['initial'] = {"modalidad": False, "secreta": False}
        super(PageForm, self).__init__(*args, **kwargs)
