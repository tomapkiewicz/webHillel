from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, Widget
from .models import Profile, PropuestaInteres


class UserCreationFormWithEmail(UserCreationForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "El email ya está registrado, probá con otro.")
        return email


class NumberInput(forms.NumberInput):
    input_type = 'number'


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'nombre', 'apellido', 'fechaNacimiento',
                  'provincia', 'whatsapp', 'instagram',
                  'onward', 'taglit', 'propuestasInteres', 'tematicasInteres', 'comoConociste',
                  'estudios', 'experienciaComunitaria',
                  'validado']
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={
                'class':
                'form-control-file mt-3'}),

            'onward': forms.Select(attrs={'class': 'form-control mt-1',
                                          'rows': 4,
                                          'placeholder': '',
                                          'initial': 'NO',
                                          'required': True}),

            'taglit': forms.Select(attrs={'class': 'form-control mt-1',
                                          'rows': 4,
                                          'placeholder': '',
                                          'required': True}),

            'propuestasInteres': forms.CheckboxSelectMultiple(
                attrs={'placeholder': '',
                       'required': False}
            ),


            'tematicasInteres': forms.CheckboxSelectMultiple(
                attrs={'placeholder': '',
                       'required': False}
            ),


            'comoConociste': forms.Textarea(attrs={'class': 'form-control mt-1',
                                                   'rows': 3,
                                                   'placeholder': '',
                                                   'required': True}),

            'instagram': forms.TextInput(attrs={'class': 'form-control mt-3',
                                                'placeholder': '@ de Instagram',
                                                'required': True}),

            'nombre': forms.TextInput(attrs={'class': 'form-control mt-3',
                                             'placeholder': 'Nombre',
                                             'required': True}),

            'apellido': forms.TextInput(attrs={'class': 'form-control mt-3',
                                               'placeholder': 'Apellido',
                                               'required': True}),

            'estudios': forms.Textarea(attrs={'class': 'form-control mt-1',
                                              'placeholder': '',
                                              'required': True}),

            'experienciaComunitaria': forms.Textarea(attrs={'class': 'form-control mt-1',
                                                            'placeholder': '',
                                                            'required': True}),

            'whatsapp': NumberInput(attrs={'class': 'form-control mt-3',
                                           'placeholder': 'Ej. BsAs: "11xxxxxxxx" ',
                                           'required': True}),
            'provincia': forms.Select(attrs={'class': 'form-control mt-1',
                                             'placeholder': '',
                                             'required': True}),

            'fechaNacimiento': TextInput(attrs={'class':
                                                'form-control mt-3',
                                                'placeholder':
                                                '*Fecha de nacimiento "dd/mm/aaaa"',
                                                'required': True}),


            'validado': forms.TextInput(attrs={'class': 'form-control mt-3',
                                               'placeholder': '',
                                               'hidden': True}),
        }

    def __init__(self, *args, **kwargs):
        if kwargs['instance'].nombre is None:
            kwargs['initial'] = {"taglit": 0, "onward": 0, "provincia": 0}
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['fechaNacimiento'].widget.format = '%d/%m/%Y'

    def clean(self):
        # Validaciones extra
        # cleaned_data = super().clean()
        if self.is_valid():
            self.cleaned_data['validado'] = True
        else:
            self.cleaned_data['validado'] = False
        return


class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        help_text="Requerido, 254 caracteres como máximo y debe ser válido")

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if 'email' in self.changed_data:
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError(
                    "El email ya está registrado, prueba con otro.")
        return email
