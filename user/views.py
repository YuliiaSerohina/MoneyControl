from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


def main_page(request):
    username = request.user.username
    return render(request, 'main_page.html', {'username': username})


def registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(name, email, password)
        user.save()
        return redirect('/')
    return render(request, 'registration.html')


def login_handler(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user/home/')
        else:
            return redirect('/')
    return render(request, 'login_handler.html')


def logout_handler(request):
    logout(request)
    return redirect('/')


