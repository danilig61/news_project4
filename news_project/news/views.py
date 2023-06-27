from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q
from .models import News, Article, Post, UserProfile
from .forms import NewsForm, ArticleForm, SignupForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def test_func(self):
        return self.request.user.groups.filter(name='authors').exists()

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            if 'become_author' in request.POST:
                authors_group = Group.objects.get(name='authors')
                user.groups.add(authors_group)
                messages.success(request, 'Your request to become an author has been submitted.')
                return redirect('profile')

            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')

@login_required
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    fields = ['first_name', 'last_name', 'email']
    template_name = 'profile.html'
    success_url = reverse_lazy('profile')




def news_list(request):
    news_list = News.objects.order_by('-published_date')
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_list.html', {'page_obj': page_obj})


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.published_date = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm()
    return render(request, 'news/news_form.html', {'form': form})


def news_edit(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == 'POST':
        form = NewsForm(request.POST, instance=news)
        if form.is_valid():
            news = form.save(commit=False)
            news.published_date = timezone.now()
            news.save()
            return redirect('news_detail', pk=news.pk)
    else:
        form = NewsForm(instance=news)
    return render(request, 'news/news_form.html', {'form': form})


def news_delete(pk):
    news = get_object_or_404(News, pk=pk)
    news.delete()
    return redirect('news_list')


def news_search(request):
    query = request.GET.get('q')
    if query:
        news_list = News.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        ).distinct()
    else:
        news_list = News.objects.all()
    paginator = Paginator(news_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'news/news_search.html', {'page_obj': page_obj, 'query': query})

class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_update.html'
    success_url = reverse_lazy('article_list')

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_update.html'
    success_url = reverse_lazy('article_list')

class ArticleCreateView(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_create.html'
    success_url = reverse_lazy('article_list')

class ArticleUpdateView(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'article_update.html'
    success_url = reverse_lazy('article_list')

class SignupView(CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return response

class AddAuthorView(View):
    def post(self, request):
        author_group = Group.objects.get(name='authors')
        author_group.user_set.add(request.user)
        return redirect('profile')