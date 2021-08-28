from django.shortcuts import render,redirect, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponse
from App_Login.forms import ProfileForm, SignUpForm
from App_Login.models import Profile, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def sign_up(request):
    form=SignUpForm
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account Created Successfully")
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/sign_up.html',context={'form':form})
def login_user(request):
    form=AuthenticationForm
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request, 'App_Login/login.html', context={'form':form})
@login_required
def logout_user(request):
    logout(request)
    messages.warning(request,"You are logged Out")
    return HttpResponseRedirect(reverse('App_Shop:home'))
@login_required
def user_profile(request):
    profile=Profile.objects.get(user=request.user)
    profile_form=ProfileForm(instance=profile)
    if request.method == 'POST':
        profile_form=ProfileForm(request.POST, request.FILES,instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request,"The changes has been updated")
            profile_form=ProfileForm(instance=profile)
            return HttpResponseRedirect(reverse('App_Shop:home'))
    return render(request,'App_Login/user_profile.html',context={'profile_form':profile_form})
