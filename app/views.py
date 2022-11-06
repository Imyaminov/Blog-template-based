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
from django.db.models import Count
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from common.models import User
from .models import Post, Category, Comment

class HomePostListView(ListView):
    model = Post
    template_name = 'app/home.html'
    context_object_name = 'posts'
    ordering = ('-created_at',)
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().annotate(posts_count=Count('post')).order_by('parent')
        return context

    def get_queryset(self):
        q = self.request.GET.get('post')

        if q:
            vector = SearchVector('title')
            query = SearchQuery(q)
            rank = SearchRank(vector, query)
            return super().get_queryset().annotate(rank=rank).filter(rank__gte=0.001).order_by('-rank')
            # return super().get_queryset().annotate(search=vector).filter(search=query)

        return super().get_queryset()

    # @method_decorator(cache_page(60*60*1))
    # def get(self, *args, **kwargs):
    #     return super().get(*args, **kwargs)

class UserPostListView(ListView):
    model = Post
    template_name = 'app/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(author__username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = User.objects.all().filter(username=self.kwargs['username'])
        context['comments'] = Comment.objects.all().filter(post__author__username=self.kwargs['username'])
        context['most_commented'] = self.get_queryset().order_by('-comments_count')[:6]
        context['user_post_count'] = Post.user_post_count(self.kwargs["username"])
        return context

class CategoryPostListView(ListView):
    model = Post
    template_name = 'app/category_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs['category_name'])

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'app/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # retrieving similar posts by tags
        post_tags_ids = context['post'].tag.values_list('id', flat=True)
        similar_posts = Post.objects.filter(tag__in=post_tags_ids).exclude(id=context['post'].id)
        context['similar_posts'] = similar_posts.annotate(same_tags=Count('tag')).order_by('-same_tags', '-created_at')[:4]
        # comments for particular post
        context['post_comment'] = Comment.objects.all().filter(post=context['post'])
        context['comment_count'] = Post.comment_count(context['post'])
        Post.save(context['post'])

        return context

    # @method_decorator(cache_page(60 * 60 * 2))
    # def get(self, *args, **kwargs):
    #     return super().get(*args, **kwargs)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('title', 'content', 'category', 'tag')
    template_name = 'app/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content', 'tag')
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
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'], 'slug': self.kwargs['slug']})

def about(request):
    return render(request, 'app/about.html', {'title': 'Post_1'})
