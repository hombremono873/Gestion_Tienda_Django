from django import forms
from django.core.validators import RegexValidator
from apps.core.constantes import TipoDocumento
from .models import Usuario
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm

solo_digitos = RegexValidator(r"^\d+$", "Escriba solo números, sin puntos ni espacios.")
telefono_valido = RegexValidator(r"^\+?\d{7,15}$", "Escriba entre 7 y 15 dígitos; puede iniciar con +.")

class RegistroForm(forms.Form):
    first_name = forms.CharField(label="Nombres", max_length=150)
    last_name = forms.CharField(label="Apellidos", max_length=150)
    telefono=forms.CharField(label="Teléfono", max_length=20, required=False, validators=[telefono_valido])
    documento=forms.CharField(label="Documento", max_length=20,validators=[solo_digitos])
    tipo_documento = forms.ChoiceField(label="Tipo de documento", choices=TipoDocumento.choices, initial=TipoDocumento.CC)
    email= forms.EmailField(label="Correo electrónico")
    
    """ strip limpia los espacioa al inicio y final de la cadea, attrs controla como se vera en html la entrada de datos"""
    password1 = forms.CharField(label="Contraseña", strip=False,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password2 = forms.CharField(label="Repita la contraseña", strip=False,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))

    def __init__(self, *args, **kwargs):
        # Aplica las clases de Bootstrap a cada campo
        super().__init__(*args, **kwargs)
        for campo in self.fields.values():
            es_lista = isinstance(campo.widget, forms.Select)
            campo.widget.attrs["class"] = "form-select" if es_lista else "form-control"

    def full_clean(self):
        # Marca en rojo los campos con error
        super().full_clean()
        for nombre in self.errors:
            if nombre in self.fields:
                self.fields[nombre].widget.attrs["class"] += " is-invalid"

    def clean_email(self):
        # Valida que el correo no exista (sin importar mayúsculas)
        correo = self.cleaned_data["email"].lower()
        if Usuario.objects.filter(email__iexact=correo).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo")
        return correo

    def clean(self):
        #Valida que el documento no exista
        datos = super().clean()
        tipo=datos.get("tipo_documento")
        numero =datos.get("documento")

        if tipo and numero and Usuario.objects.filter(tipo_documento=tipo, documento=numero).exists():
            self.add_error("documento","Ya existe una cuenta con este documento")
        p1 = datos.get("password1") 
        p2 = datos.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Las contraseñas no coinciden")
        elif p1:
            # Aplica las reglas de AUTH_PASSWORD_VALIDATORS de settings.py:
            # largo mínimo, no muy común, no solo números, no parecida al nombre o correo
            borrador = Usuario(email=datos.get("email", ""),
                               first_name=datos.get("first_name", ""),
                               last_name=datos.get("last_name", ""))
            try:
                password_validation.validate_password(p1, borrador)
            except forms.ValidationError as error:
                self.add_error("password1", error)

        return datos

class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "El correo o la contraseña son inválidos.",
        "inactive": "Esta cuenta está desactivada.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label="Correo electrónico"

        for campo in self.fields.values():
            campo.widget.attrs["class"]="form-control"
            
        
