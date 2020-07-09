from django.shortcuts import render, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .forms import UpdateUserProfile, RegisterNewUser

# Create your views here.


def userLogin(request):
    form = UpdateUserProfile()
    return render(request, 'user_auth/login.html', {'form': form})


def userLogout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_auth:login'))


def register(request):
    form = RegisterNewUser()
    return render(request, 'user_auth/register.html', {'form': form})


def registerUser(request):
    if request.method == "POST":
        form = RegisterNewUser(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            try:
                user = User.objects.get(username=username)
            except (KeyError, User.DoesNotExist):
                user = User.objects.create_user(
                    username=username,
                    password=password,
                )
                user.save()
                return HttpResponseRedirect(reverse('hub:home'))
            else:
                return render(request, 'user_auth/error.html', {
                    'error_message': "The username already exists.",
                })

def authUser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('hub:home'))
        else:
            return render(request, "user_auth/error.html", {
                'error_message': "The username / password is incorrect.",
            })
