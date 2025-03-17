from django.shortcuts import render, redirect


def admin_user_list(request):
    return render(request, 'adminUsers/list.html')


def register_admin_user(request):
    return render(request, 'adminUsers/register_admin_user.html')


def reset_password(request):
    return render(request, 'adminUsers/reset_password.html')


def d_reset_password(request):
    return render(request, 'adminUsers/d_reset_password.html')


def forgot_password(request):
    return render(request, 'adminUsers/forgot_password.html')


def login(request):
    return redirect('dashboard')


def logout(request):
    return render(request, 'adminUsers/login.html')
