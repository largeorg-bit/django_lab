from django import forms
from django.core.exceptions import ValidationError

from catalog.models import ContactMessage, Product

FORBIDDEN_WORDS = (
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ("name", "phone", "message")
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваше имя",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Контактный телефон",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Ваше сообщение",
                    "rows": 4,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True
            field.error_messages["required"] = "Это поле обязательно."


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "image",
            "category",
            "price",
            "is_available",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"

            if field_name in ("name", "description", "category", "price"):
                field.required = True
                field.error_messages["required"] = "Это поле обязательно."

    def _validate_forbidden_words(self, value, field_label):
        text = value.lower()
        for word in FORBIDDEN_WORDS:
            if word in text:
                raise ValidationError(
                    f'В поле «{field_label}» нельзя использовать '
                    f'запрещённое слово «{word}».'
                )
        return value

    def clean_name(self):
        name = self.cleaned_data["name"]
        return self._validate_forbidden_words(name, "Наименование")

    def clean_description(self):
        description = self.cleaned_data["description"]
        return self._validate_forbidden_words(description, "Описание")

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError(
                "Цена не может быть отрицательной. "
                "Укажите значение больше или равное нулю."
            )
        return price
