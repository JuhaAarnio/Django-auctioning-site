from django import forms


class SignUpForm(forms.Form):
    username = forms.CharField(label='username', max_length=32)
    password = forms.CharField(label='password', max_length=256)
    email = forms.CharField(label='email', max_length=256)


class SignInForm(forms.Form):
    username = forms.CharField(label='username', max_length=32)
    password = forms.CharField(label='password', max_length=256)


class EditUserForm(forms.Form):
    new_email = forms.CharField(label="new email", max_length=256)
    new_password = forms.CharField(label="new password", max_length=256)