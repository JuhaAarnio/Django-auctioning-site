from django.views import View
from django.shortcuts import render


class SignUp(View):
    def get_signup(request):
        render(request, 'user/signup.html', {})


class SignIn(View):
    pass


def signout(request):
    pass


class EditProfile(View):
    pass
