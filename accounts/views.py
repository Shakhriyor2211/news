from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, TemplateView, CreateView, View

from accounts.forms import RegisterForm, LoginForm, RegisterCustomForm, UserEditForm, ProfileEditForm
from accounts.models import Profile


def loginPageView(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data["username"], password=data["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("landing_page")
                else:
                    return HttpResponse("User is not active")

            else:
                return HttpResponse("Username or password incorrect")
    else:
        form = LoginForm()
        context = {
            "form": form
        }
        return render(request, 'registration/login.html', context)


class ProfilePageView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            'user_form': UserEditForm(instance=request.user),
            'profile_form': ProfileEditForm(instance=request.user.profile)
        }
        return render(request, 'profile.html', context)

    def post(self, request):
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        context = {"user_form": user_form, "profile_form": profile_form}
        if user_form.is_valid() and profile_form.is_valid():
            new_form = user_form.save(commit=False)
            profile_form = profile_form.save(commit=False)
            new_form.save()
            profile_form.save()
            return redirect("landing_page")
        return render(request, "profile.html", context)


@login_required
def profilePageView(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("landing_page")

        return render(request, 'profile.html', context)
    else:
        context = {
            'user_form': UserEditForm(instance=request.user),
            'profile_form': ProfileEditForm(instance=request.user.profile)
        }
    return render(request, 'profile.html', context)

def registerPageView(request):
    if request.method == "POST":
        user_form = RegisterCustomForm(request.POST)
        context = {"form": user_form}
        if user_form.is_valid():
            new_form = user_form.save(commit=False)
            new_form.set_password(user_form.cleaned_data['password1'])
            new_form.save()
            Profile.objects.create(user=new_form)
            return redirect("login_page")
        return render(request, "registration/register.html", context)
    else:
        context = {
            'form': RegisterCustomForm()
        }
        return render(request, 'registration/register.html', context)


# class RegisterPageView(View):
#     def get(self, request):
#         context = {
#             'form': RegisterCustomForm()
#         }
#         return render(request, 'registration/register.html', context)
#
#     def post(self, request):
#         user_form = RegisterCustomForm(request.POST)
#         context = {"form": user_form}
#         if user_form.is_valid():
#             new_form = user_form.save(commit=False)
#             new_form.set_password(user_form.cleaned_data['password1'])
#             new_form.save()
#             return redirect("login_page")
#         return render(request, "registration/register.html", context)

class RegisterPageView(LoginRequiredMixin, CreateView):
    form_class = RegisterCustomForm
    success_url = reverse_lazy('login_page')
    template_name = "registration/register.html"
