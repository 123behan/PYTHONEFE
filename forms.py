from django import forms

class UserLoginForm(forms.Form):
    username=forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder':'Your Username',
                'autocomplete':'off',
            }
        )
    )
    password= forms.CharField( required=True,widget=forms.PasswordInput(
        attrs={
            'id':'password_id',
        }
    )
    )

    show= forms.BooleanField(
        label='Show Password',
        widget=forms.CheckboxInput(
            attrs={
                'class':'show-password',
            }
        ),
        required=False
    )