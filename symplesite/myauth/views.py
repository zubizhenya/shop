from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView




class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user  # Получаем текущего пользователя
        context['user'] = user  # Передаем только текущего пользователя в контекст
        return context
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(self.request, username=username, password=password,)
        if user is not None:
            login(self.request, user)
        return response

def login_view(request:HttpRequest):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('about-me')
        return render(request, 'myauth/login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('about-me')
    return render(request,"myauth/login.html", {"error":"Invalid login"})

def logout_view(request:HttpRequest):
    logout(request)
    return redirect('index')

class PasswordChangeView(PasswordChangeView):
    template_name = 'myauth/passwordchange.html'
    success_url = reverse_lazy('about-me')
    form_class = PasswordChangeForm
    def form_valid(self, form):
        user = self.request.user
        if user.check_password(form.cleaned_data['old_password']):
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error('old_password', 'Текущий пароль неверен.')
            return self.form_invalid(form)

