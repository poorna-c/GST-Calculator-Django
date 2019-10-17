from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileUpdateForm, UserUpdateForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import profile

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for User {username}. Now you can login to your account.")
            return redirect('login_page')
        else:
            messages.warning(request,f"User Not Created! Resolve The Following Issues and Try Again")
    else:
        form = UserRegistrationForm()
    return render(request,'accounts/register.html',{'form':form,'title':'Register'})

@login_required
def profile(request):
    if request.user.profile.first_login_ip == None:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        request.user.profile.first_login_ip = ip
        request.user.profile.save()

    if request.method == "POST":
        print(request.POST)
        profile_form = ProfileUpdateForm(request.POST,instance = request.user.profile)
        user_form = UserUpdateForm(request.POST, instance = request.user)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Account Updated successfully.")
            return redirect('profile_page')
    else:
        profile_form = ProfileUpdateForm(instance = request.user.profile)
        user_form = UserUpdateForm(instance = request.user)
    
    return render(request,'accounts/profile.html',{'profile_form':profile_form,'user_form':user_form, 'title':f'Profile - {request.user.username}'})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return HttpResponse("YOUR IP ADDRESS = ",ip)

