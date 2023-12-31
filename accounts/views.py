from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from accounts.forms import LoginForm, SignupForm


def custom_login(request: HttpRequest) -> HttpResponse:
    form = LoginForm()
    context = {
        "form": form
    }
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("spa-comments:home"))
            else:
                context["message"] = "User with provided credentials not found!"
        else:
            context["form_error"] = form.errors
    return render(request, "registration/login.html", context=context)


def signup(request: HttpRequest) -> HttpResponse:
    form = SignupForm()
    context = {
        "form": form
    }

    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password1"]

            form.cleaned_data.pop("password1")
            form.cleaned_data.pop("password2")

            user = get_user_model().objects.create_user(password=password, **form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(reverse_lazy("spa-comments:home"))
            else:
                context["message"] = "Cannot sign up with provided credentials!"
        else:
            context["form_error"] = form.errors
    return render(request, "registration/signup.html", context=context)
