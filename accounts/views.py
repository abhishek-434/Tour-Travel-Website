from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import (
    LoginView, PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from .forms import RegistrationForm, LoginForm

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard:profile')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, f"Welcome to Wanderlust, {user.first_name}! Your account has been registered.")
            return redirect('dashboard:profile')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegistrationForm()
        
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        messages.success(self.request, f"Welcome back, {self.request.user.first_name or self.request.user.username}!")
        return reverse_lazy('dashboard:profile')


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have logged out of your Wanderlust session.")
    return redirect('core:home')


# Password Reset Views with customized glass templates
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
