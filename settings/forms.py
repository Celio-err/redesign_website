from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm


class UserCreateWithRoleForm(UserCreationForm):
    username = forms.CharField(
        label="Nome de Utilizador",
        help_text="",
    )
    email = forms.EmailField(
        label="Email",
        help_text="",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="Palavra-passe",
        help_text="",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirmar Palavra-passe",
        help_text="",
    )
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Role",
        required=True,
        help_text="Escolha o nível de acesso deste utilizador."
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            role = self.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
        return user


class UserEditForm(forms.ModelForm):
    username = forms.CharField(
        label="Nome de Utilizador",
        help_text="",
    )
    email = forms.EmailField(
        label="Email",
        help_text="",
    )
    nova_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Palavra-passe",
        help_text="",
    )
    confirmar_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirmar Palavra-passe",
        help_text="",
    )
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        label="Role",
        required=True,
        help_text="Escolha o nível de acesso deste utilizador."
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            current_group = self.instance.groups.first()
            if current_group:
                self.fields['role'].initial = current_group

    def clean(self):
        cleaned_data = super().clean()
        nova_password = cleaned_data.get('nova_password')
        confirmar_password = cleaned_data.get('confirmar_password')

        if nova_password or confirmar_password:
            if nova_password != confirmar_password:
                raise forms.ValidationError("As palavras-passe não coincidem.")
            if len(nova_password) < 8:
                raise forms.ValidationError("A palavra-passe deve ter no mínimo 8 caracteres.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        nova_password = self.cleaned_data.get('nova_password')
        if nova_password:
            user.set_password(nova_password)
        if commit:
            user.save()
            role = self.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
        return user