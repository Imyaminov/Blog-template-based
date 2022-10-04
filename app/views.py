from django.shortcuts import render
from django.urls import reverse, reverse_lazy
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
from django.views.generic.edit import FormMixin
from .models import Post, Category, Comment
from .forms import CommentForm

class HomePostListView(ListView):
    queryset = Post.objects.all()
    template_name = 'app/home.html'
    ordering = ('-created_at',)
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('parent')
        return context

    def get_queryset(self):
        query = self.request.GET.get('post')
        if query:
            return super().get_queryset().filter(title__icontains=query)
        else:
            return super().get_queryset()

class UserPostListView(ListView):
    model = Post
    template_name = 'app/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(author__username=self.kwargs['username'])

class CategoryPostListView(ListView):
    model = Post
    template_name = 'app/category_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(category__title=self.kwargs['category_name'])

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['post_comment'] = Comment.objects.all().filter(post=context['post'])
        context['comment_count'] = Comment.objects.all().filter(post=context['post']).count()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content', 'category')
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

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'app/comment_create.html'
    fields = ('content',)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk']})

def about(request):
    return render(request, 'app/about.html', {'title': 'Post_1'})
