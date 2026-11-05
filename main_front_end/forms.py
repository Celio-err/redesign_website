from django import forms
from django.utils.translation import gettext_lazy as _
from contacto.models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"maxlength": 50, "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "body": forms.Textarea(attrs={"maxlength": 500, "rows": 5}),
        }
        error_messages = {
            "name": {"required": _("Escreva o seu nome.")},
            "body": {
                "required": _("Escreva o seu comentário."),
                "max_length": _("O comentário pode ter no máximo 500 caracteres."),
            },
        }

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean_body(self):
        body = self.cleaned_data["body"].strip()
        if len(body) < 3:
            raise forms.ValidationError(_("O comentário é demasiado curto."))
        return body