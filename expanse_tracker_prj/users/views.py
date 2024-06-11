from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegistrationForm
from .models import Profile
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

# Create your views here.
def user_login(request):
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            user = authenticate(request,username=data['username'],password=data['password'])
            if user is not None:
                login(request,user)
                return redirect("index")
            else:
                return HttpResponse("Invalid credentials")
    else:
        login_form = UserLoginForm()
    return render(request, 'users/login.html', {'login_form': login_form})

def user_register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user = new_user)
            return HttpResponse("User is registered")
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'user_form': form})

@receiver(user_signed_up)
def create_profile_on_social_signup(request, user, **kwargs):
    Profile.objects.get_or_create(user=user)