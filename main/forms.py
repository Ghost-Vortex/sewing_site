from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=150, label="Имя")
    contact = forms.CharField(max_length=255, label="Контакт")
    message = forms.CharField(
        label="Сообщение",
        widget=forms.Textarea,
        required=False,
    )
