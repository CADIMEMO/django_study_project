from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.views import LogoutView, TemplateView
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from .models import Profile

# Create your views here.


class RegisterView(CreateView):

    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):

        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(request=self.request, user=user)

        return response


class AboutMeView(TemplateView):
    template_name = 'myauth/about-me.html'

def login_view(request: HttpRequest):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')
    
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {"error": "Invalid login credentials"})


@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest):
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request: HttpRequest):
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value = {value!r}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest):
    request.session['foobar'] = 'spameggs'
    return HttpResponse('session set!')


@login_required
def get_session_view(request: HttpRequest):
    value = request.session.get('foobar', 'default')
    return HttpResponse(f'session value = {value!r}')


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(LogoutView):
     next_page = reverse_lazy('myauth:login')


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})

