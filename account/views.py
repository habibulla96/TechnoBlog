from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .models import User
from .foms import RegistrationForm


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'account/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('home')
    success_message = 'Вы успешно зарегистрированы!'


class SignInView(LoginView):
    template_name = 'account/login.html'


class LogoutView(LogoutView):
    template_name = 'home'
    success_message = 'Вы вышли с аккаунта'


def profile(requset):
    return render(requset, 'account/profile.html')
