from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.utils.decorators import method_decorator
from .forms import SignUpForm, SignInForm, EditUserForm
from django.contrib import auth, messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.translation import gettext as _


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {"form": SignUpForm})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            b_username = cd["username"]
            b_password = cd["password"]
            b_email = cd["email"]
            if User.objects.filter(username=b_username).exists():
                messages.add_message(request, messages.INFO, _("This username has been taken"))
                return render(request, 'signup.html', {"form": SignUpForm})
            if User.objects.filter(email=b_email).exists():
                messages.add_message(request, messages.INFO, _("This email has been taken"))
                return render(request, 'signup.html', {"form": SignUpForm}, status=200)
            else:
                User.objects.create_user(b_username, b_password, b_email)
                return HttpResponseRedirect(reverse("home"))
        else:
            return HttpResponse(status=200)



class SignIn(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', {"form": SignInForm})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            b_username = user_data["username"]
            b_password = user_data["password"]
            user = auth.authenticate(request, username=b_username, password=b_password)
            if user is not None:
                auth.login(request, user)
                messages.add_message(request, messages.INFO, _("Logged in"))
                return render(request, "home.html")
            else:
                messages.add_message(request, messages.INFO, _("Invalid username or password"))
                return render(request, "signin.html", {"form": SignInForm})
        else:
            return render(request, "trololoo.html")



@login_required
def signout(request):
    auth.logout(request)
    messages.add_message(request, messages.INFO, _("Logged out"))
    return HttpResponseRedirect(reverse("home"))


@method_decorator(login_required, name='dispatch')
class EditProfile(View):
    def get(self, request):
        if auth.user_logged_in:
            return render(request, "edituser.html", {"form": EditUserForm})



    def post(self, request):
        form = EditUserForm(request.POST)
        user = request.user
        if form.is_valid():
            cd = form.cleaned_data
            np = cd["new_password"]
            ne = cd["new_email"]
            if User.objects.filter(email=np).exists():
                messages.add_message(request, messages.INFO, _("Email already taken"))
                return render(request, "edituser.html", {"form": EditUserForm})
            else:
                user.set_password(np)
                user.email = ne
                user.save()
                return render(request, "home.html")


class Home(View):
    def get(self, request):
        return render(request, 'home.html')
