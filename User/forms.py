from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField

class PasswordResetForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    # add morjor field when implemented
    new_password = forms.CharField(max_length=50, widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        max_length=50, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )
        return cleaned_data


class LoginForm(AuthenticationForm):
    class Meta:
        widgets = {
            'id_username': forms.TextInput(attrs={'placeholder':'username','class':'user','size':25,'maxlength':50,'autocomplete':'off','required':'required'})
        }