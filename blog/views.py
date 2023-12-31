from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post
from django.contrib.auth.models import User
from django.views import generic
from django.urls import reverse_lazy

# Create your views here.


class PostListView(generic.ListView):
    template_name = "blog/home.html"
    model = Post
    context_object_name = "posts"
    # ordering = ["-date_posted"]
    paginate_by = 5

    def get_queryset(self):
        if "q" in self.request.GET:
            return Post.objects.filter(
                title__icontains=self.request.GET.get("q")
            ).order_by("-date_posted")
        return Post.objects.all().order_by("-date_posted")


class UserPostListView(generic.ListView):
    template_name = "blog/user_posts.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy("blog-home")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
