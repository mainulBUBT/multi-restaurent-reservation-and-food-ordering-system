from urllib import request
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from App_Login.forms import UserForm, ProfilePicForm, UserProfileChangeForm, UserProfileChangeForm_2
from App_Login.models import UserInfo


# Create your views here.


def register(request):
    form = UserForm()
    if request.method == 'POST':
            form = UserForm(data=request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Account Created Successfully!")
                return HttpResponseRedirect(reverse('App_Login:register'))

    return render(request, 'App_Login/registration.html', context={'form':form})

def login_page(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/login.html', context={'form': form})


def home(request):
    return render(request, 'App_Login/profile.html')

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))

@login_required
def add_pro_pic(request):
    form = ProfilePicForm()

    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES)
        if form.is_valid():
            user_object = form.save(commit=False)
            user_object.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))

    return render(request, 'App_Login/add_pro_pic.html', context={'form': form})

@login_required
def change_pro_pic(request):
    form = ProfilePicForm(instance=request.user.user_info)
    if request.method == 'POST':
        form = ProfilePicForm(request.POST, request.FILES, instance=request.user.user_info)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/add_pro_pic.html', context={'form':form})

def user_change(request):
    current_user = request.user
    form_1 = UserProfileChangeForm(instance=current_user)
    user_info = UserInfo.objects.filter(user=current_user).first()
    form_2 = UserProfileChangeForm_2(instance=user_info)

    if request.method == 'POST':
        form_1 = UserProfileChangeForm(request.POST, instance=current_user)
        form_2 = UserProfileChangeForm_2(request.POST, instance=user_info)
        if form_1.is_valid() and form_2.is_valid():
            form_1.save()
            form_2.save()
            form_1= UserProfileChangeForm(instance=current_user)
            form_2= UserProfileChangeForm_2(instance=user_info)
            messages.success(request, "Profile Updated Successfully!")
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/change_profile.html', context={'form_1': form_1,'form_2': form_2})

def change_pass(request):
    current_user = request.user
    form = PasswordChangeForm(current_user)
    changed = False

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user= current_user)
        if form.is_valid():
            form.save()
            messages.success(request, "Password Updated Successfully. Login Now")
            return HttpResponseRedirect(reverse('App_Login:login'))
    return render(request, 'App_Login/change_pass.html', context={'form': form, 'changed':changed})