from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from spa_comments.forms import CommentCreateForm
from spa_comments.models import Comment, Author


def index(request: HttpRequest) -> HttpResponse:
    comments = Comment.objects.all()

    context = {
        "comments": comments,
        "user": request.user
    }
    return render(request, "index.html", context=context)


class CommentCreateView(generic.CreateView):
    model = Comment
    template_name = "comments_create.html"
    form_class = CommentCreateForm
    success_url = reverse_lazy("spa-comments:home")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user_data = {
                "username": request.user.username,
                "email": request.user.email,
            }
            form = self.form_class(initial=user_data)
        else:
            form = self.form_class
        return render(request, "comments_create.html", {"form": form})

    def form_valid(self, form):
        try:
            author = Author.objects.get(email=form.cleaned_data["email"])
        except Author.DoesNotExist:
            author = Author.objects.create(
                email=form.cleaned_data["email"],
                username=form.cleaned_data["username"],
                user=self.request.user
            )

        form.instance.author = author

        return super().form_valid(form)


class CommentListView(generic.ListView):
    model = Comment
    template_name = "index.html"
    queryset = Comment.objects.all()
    context_object_name = "comments"

    def get_queryset(self):
        if (self.request.user and self.request.user.is_authenticated
                and "my" in self.request.path):
            return self.queryset.filter(author__user=self.request.user)

        return self.queryset


