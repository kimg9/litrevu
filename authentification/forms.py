from django import forms
from authentification.models import User
from django.utils.translation import gettext as _


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class InscriptionForm(LoginForm):
    confirm_password = forms.CharField(
        label="Confirmer le mot de passe", widget=forms.PasswordInput
    )
    MIN_LENGHT = 8

    def clean(self):
        cleaned_data = super(InscriptionForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        errors = []

        if password == username:
            errors.append(
                forms.ValidationError(
                    _(
                        "L'utilisateur et le mot de passe ne peuvent pas être identiques."
                    ),
                    code="same_user_pass",
                )
            )

        if password != confirm_password:
            errors.append(
                forms.ValidationError(
                    _("Les mots de passe ne correspondent pas."), code="mismatched_pass"
                )
            )

        if len(password) < self.MIN_LENGHT:
            errors.append(
                forms.ValidationError(
                    _(
                        "Le mot de passe doit avoir au moins %(min_lenght)s charactères."
                    ),
                    params={"min_lenght": self.MIN_LENGHT},
                    code="wrong_lenght",
                )
            )

        if not any(
            ch in password
            for ch in [
                "~",
                "`",
                "!",
                "@",
                "#",
                "$",
                "%",
                "^",
                "&",
                "*",
                "(",
                ")",
                "_",
                "-",
                "+",
                "=",
                "{",
                "[",
                "}",
                "]",
                "|",
                "\\",
                ":",
                ";",
                "'",
                "<",
                ",",
                ">",
                ".",
                "?",
                "/",
                "]",
                '"',
            ]
        ):
            errors.append(
                forms.ValidationError(
                    _(
                        "Le mot de passe doit contenir au moins l'un de ces caractères spéciaux : ~`!@#$%^&*()_-+={[}]|\\:;\"'<,>.?/"
                    ),
                    code="special_char",
                )
            )

        if not any(map(str.isupper, password)):
            errors.append(
                forms.ValidationError(
                    _("Le mot de passe doit contenir au moins une lettre majuscule."),
                    code="uppercase",
                )
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            errors.append(
                forms.ValidationError(
                    _("username already exists"), code="existing_user"
                )
            )

        if errors:
            raise forms.ValidationError(errors)
