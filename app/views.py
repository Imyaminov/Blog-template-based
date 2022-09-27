from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post

class HomeListView(ListView):
    model = Post
    template_name = 'app/home.html'
    context_object_name = 'posts'
    paginate_by = 5

    # given 3 ways of ordering
    ordering = ('-created_at',)
    # queryset = Post.objects.all().order_by('-created_at')
    # def get_queryset(self):
    #     return super().get_queryset().order_by('-created_at')

class UserPostListView(ListView):
    model = Post
    template_name = 'app/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(author__username=self.kwargs['username'])

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content',)
    template_name = 'app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content',)
    template_name = 'app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'app/post_delete.html'
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        if post.author == self.request.user:
            return True
        return False

    def get_success_url(self):
        return reverse('blog-home')

def about(request):
    return render(request, 'app/about.html', {'title': 'Post_1'})
