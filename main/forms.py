from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, PuntoUsuario
from django.contrib.auth import login  


class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'family_name', 'second_family_name']
        labels = {
            'email': 'Correo Electrónico',
            'first_name': 'Nombre',
            'family_name': 'Primer apellido',
            'second_family_name': 'Segundo apellido',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['family_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['second_family_name'].widget.attrs.update({'class': 'form-control'})

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validate_password(password1, self.instance)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

        if password1:
            if len(password1) < 8:
                raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres.")

            has_letter = False
            has_digit = False
            for char in password1:
                if char.isalpha():
                    has_letter = True
                elif char.isdigit():
                    has_digit = True

            if not (has_letter and has_digit):
                raise forms.ValidationError("La contraseña debe contener al menos una letra y un número.")
    
    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password1'])
            user.save()
        if request:
            login(request, user)
        return user


class InicioSesionForm(forms.Form):
    email = forms.EmailField(
        label='Correo Electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    



        
