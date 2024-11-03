from django import forms

class LoginForms(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",  # Atualize para 'form-input'
                "placeholder": "Ex.: joaosilva@gmail.com"
            }
        )
    )
    senha = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",  # Atualize para 'form-input'
                "placeholder": "Ex.: Digite sua senha"
            }
        )
    )

class CadastroForms(forms.Form):
    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-input",  # Atualize para 'form-input'
                "placeholder": "Ex.: joaosilva@gmail.com"
            }
        )
    )
    senha1 = forms.CharField(
        label="Senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",  # Atualize para 'form-input'
                "placeholder": "Ex.: Digite sua senha"
            }
        )
    )
    senha2 = forms.CharField(
        label="Confirmação de senha",
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-input",  # Atualize para 'form-input'
                "placeholder": "Ex.: Digite sua senha novamente"
            }
        )
    )
        
    def clean_senha2(self):
        senha1 = self.cleaned_data.get("senha1")
        senha2 = self.cleaned_data.get("senha2")

        if senha1 and senha2:
            if senha1 != senha2:
                raise forms.ValidationError("As senhas não são iguais!")
            else:
                return senha2
