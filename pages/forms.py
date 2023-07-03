from django import forms
from .models import Page
from .models import RecurrentPage
from django.core.validators import MinValueValidator

class PageForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['title', 'description', 'textoExtraMail','con_mail_personalizado', 'asunto_mail', 'cuerpo_mail' ,'fecha', 'horaDesde', 'horaHasta', 'flyer', 'cupo',
                  'modalidad', 'categories', 'provincia','con_preinscripcion', 'secreta', 'clave' , 'responsable', 'colaborador']
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Título'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'textoExtraMail': forms.Textarea(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Fecha', 'type': 'date', 'format': '%d-%m-%Y'}),
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
        instance = kwargs.get('instance')  # Use get() method to safely retrieve the instance
        if instance is not None:
            if instance.modalidad is None:
                kwargs.setdefault('initial', {})["modalidad"] = False
            if instance.secreta is None:
                kwargs.setdefault('initial', {})["secreta"] = False
        else:
            kwargs.setdefault('initial', {})["modalidad"] = False
            kwargs.setdefault('initial', {})["secreta"] = False
        super(PageForm, self).__init__(*args, **kwargs)

class RecurrentPageForm(forms.ModelForm):
    dias = forms.MultipleChoiceField(
        label="Días",
        choices=RecurrentPage.DIAS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
    )
    class Meta:
        model = RecurrentPage
        fields = ['title', 'horaDesde', 'horaHasta', 'description', 'textoExtraMail', 'con_mail_personalizado',
                  'asunto_mail', 'cuerpo_mail', 'flyer', 'fechaDesde', 'fechaHasta','dias', 'cupo', 'modalidad', 'nuevo',
                  'activa', 'categories', 'provincia', 'responsable', 'colaborador', 'secreta', 'clave',
                  'con_preinscripcion']
        widgets = {
            'title': forms.TextInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Título'}),
            'horaDesde': forms.TimeInput(format="%H:%M", attrs={'type': 'time', 'required': True}),
            'horaHasta': forms.TimeInput(format="%H:%M", attrs={'type': 'time', 'required': True}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'textoExtraMail': forms.Textarea(attrs={'class': 'form-control'}),
            'con_mail_personalizado': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'asunto_mail': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto del mail'}),
            'cuerpo_mail': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Cuerpo del mail'}),
            'flyer': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Flyer'}),
            'fechaDesde': forms.DateInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Fecha desde', 'type': 'date'}),
            'fechaHasta': forms.DateInput(attrs={'required': True, 'class': 'form-control', 'placeholder': 'Fecha hasta', 'type': 'date'}),
            'cupo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cupo', 'min': '0'}),
            'modalidad': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'nuevo': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'provincia': forms.Select(attrs={'class': 'form-control'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'colaborador': forms.Select(attrs={'class': 'form-control'}),
            'secreta': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'clave': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave'}),
            'con_preinscripcion': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Título',
            'horaDesde': 'Hora desde',
            'horaHasta': 'Hora hasta',
            'description': 'Descripción',
            'textoExtraMail': 'Texto extra del mail',
            'con_mail_personalizado': 'Con mail personalizado',
            'asunto_mail': 'Asunto del mail',
            'cuerpo_mail': 'Cuerpo del mail',
            'flyer': 'Flyer',
            'fechaDesde': 'Fecha desde',
            'fechaHasta': 'Fecha hasta',
            'cupo': 'Cupo',
            'modalidad': 'Es Online?',
            'nuevo': 'Nuevo',
            'activa': 'Activa',
            'categories': 'Categorías',
            'provincia': 'Provincia',
            'dias': 'Días',
            'responsable': 'Responsable',
            'colaborador': 'Colaborador',
            'secreta': 'Privada',
            'clave': 'Clave',
            'con_preinscripcion': 'Con preinscripción',
        }
        validators = {
            'cupo': [MinValueValidator(0)],
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.dias = ','.join(self.cleaned_data['dias'])  # Convert list to comma-separated string
        if commit:
            instance.save()
        return instance