from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Libro

class RegistroUsuarioForm(UserCreationForm):
    dni = forms.CharField(max_length=20, required=True, help_text='Requerido. Ingrese su DNI.')
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'dni', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'descripcion', 'imagen')
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }