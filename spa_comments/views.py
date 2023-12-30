from __future__ import annotations

from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from spa_comments.forms import CommentCreateForm
from spa_comments.models import Comment, Author


def get_user_data(request: HttpRequest) -> dict:
    """Extracts user information from request if user is authenticated"""
    if request.user.is_authenticated:
        return {
            "username": request.user.username,
            "email": request.user.email,
        }
    return {}


class CommentCreateView(generic.CreateView):
    model = Comment
    template_name = "comments_create.html"
    form_class = CommentCreateForm
    success_url = reverse_lazy("spa-comments:home")

    def get(self, request, *args, **kwargs):
        prefill_data = get_user_data(request)

        parent_comment_id = kwargs.get("pk", None)
        if parent_comment_id:
            prefill_data["parent_comment_id"] = parent_comment_id

        return render(
            request,
            "comments_create.html",
            {"form": self.form_class(initial=prefill_data)}
        )

    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, id=form.cleaned_data.pop("parent_comment_id"))
        form.cleaned_data.pop("captcha")
        try:
            author = Author.objects.get(email=form.cleaned_data.pop("email"))
            form.cleaned_data.pop("username")
        except Author.DoesNotExist:
            author = Author.objects.create(
                email=form.cleaned_data.pop("email"),
                username=form.cleaned_data.pop("username"),
                user=self.request.user
            )

        form.instance.author = author
        form.instance.parent_comment = parent_comment

        return super().form_valid(form)


class CommentListView(generic.ListView):
    model = Comment
    template_name = "index.html"
    queryset = Comment.objects.filter(parent_comment=None)
    context_object_name = "comments"
    ordering = "-published_at"
    paginate_by = 25

    def get_queryset(self):
        queryset = self.queryset
        ordering = self.get_ordering()

        if "username" in ordering:
            ordering = ordering.replace("username", "author__username")
        elif "email" in ordering:
            ordering = ordering.replace("email", "author__email")

        if (self.request.user and self.request.user.is_authenticated
                and "my" in self.request.path):
            queryset = queryset.filter(author__user=self.request.user)

        return queryset.order_by(ordering)

    def get_ordering(self):
        ordering = self.request.GET.get("order_by", self.ordering)

        allowed_attributes = [
            "username", "-username", "email", "-email",
            "published_at", "-published_at"
        ]

        if ordering not in allowed_attributes:
            ordering = self.ordering

        return ordering

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_choice"] = self.get_ordering()
        return context
