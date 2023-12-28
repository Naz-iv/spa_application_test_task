from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from spa_comments.forms import LoginForm, SignupForm
from spa_comments.models import Comment


def index(request: HttpRequest) -> HttpResponse:
    comments = Comment.objects.all()

    context = {
        "comments": comments,
        "user": request.user
    }
    return render(request, "index.html", context=context)


def login(request: HttpRequest) -> HttpResponse:
    context = {
        "form": LoginForm()
    }
    return render(request, "login.html", context=context)


def signup(request: HttpRequest) -> HttpResponse:
    context = {
        "form": SignupForm()
    }
    return render(request, "signup.html", context=context)


def logout(request: HttpRequest) -> HttpResponse:
    pass


class CommentCreateView(generic.CreateView):
    pass


class CommentListView(generic.ListView):
    pass
