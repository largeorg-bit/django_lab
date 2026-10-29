from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "phone", "country", "avatar", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            "email": "Электронная почта",
            "phone": "Номер телефона",
            "country": "Страна",
            "password1": "Пароль",
            "password2": "Подтверждение пароля",
        }
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs["class"] = "form-control"
                if field_name in placeholders:
                    field.widget.attrs["placeholder"] = placeholders[field_name]


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Электронная почта",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].widget.attrs.update(
            {
                "class": "form-control",
                "placeholder": "Пароль",
            }
        )
        self.fields["password"].label = "Пароль"
