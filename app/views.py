from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Article, Comment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, AddPostForm, CommentForm, UpdateViewForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from .forms import CustomLoginForm
from django.utils import timezone
from datetime import timedelta

class MainView(LoginRequiredMixin,ListView):
    model = Article
    template_name = "docs/main.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for article in context['articles']:
            article.comments_count = article.comments.count()
        return context

def loginPage(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('MainView') 
            else:
                messages.error(request, "Błędna nazwa użytkownika lub hasło.")
    else:
        form = CustomLoginForm()

    return render(request, 'docs/login_page.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('MainView')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, "Invalid username or password. Try again.")
    else:
            form = RegisterForm()
    return render(request, 'docs/register_page.html', {'form': form})

class AddPost(LoginRequiredMixin, CreateView):
    model = Article
    form_class = AddPostForm
    template_name = 'docs/add_post.html'
    success_url = reverse_lazy('MainView')

    def handle_no_permission(self):
        messages.error(self.request, "You have to login if you want to add posts.")
        return super().handle_no_permission()

    def form_valid(self, form):
        now = timezone.now()

        last_post = Article.objects.filter(author=self.request.user).order_by('-created_at').first()
        
        if last_post and now - last_post.created_at < timedelta(hours=24):
            messages.error(self.request, "Możesz dodać tylko jeden post na 24 godziny.")
            return redirect('AddPost')

        form.instance.author = self.request.user
        return super().form_valid(form)
    

class DeletePost(LoginRequiredMixin,DeleteView):
    model = Article
    success_url = reverse_lazy('MainView')
    template_name = "docs/delete_view.html"


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = UpdateViewForm
    success_url = reverse_lazy('MainView')
    template_name = "docs/update_view.html"

@login_required
def MyPosts(request, username):
    if not request.user.is_authenticated:
        messages.error(request, "If you want to view posts, you have to login.")
        return redirect('register')
    else:
        user = get_object_or_404(User, username=username)
        posts = Article.objects.filter(author=user)
        return render(request, 'docs/my_posts.html', {'posts': posts})
        

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    template_name = 'docs/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added succesfully.')
            return redirect('post_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)

@login_required
def search(request):
    if request.method == "POST":
        searched = request.POST.get("searched", "")
        searched = Article.objects.filter(topic__icontains=searched)
        
        if not searched:
            messages.success(request, "That product does not exist... Try again")
            return render(request, "docs/search.html", {"searched": searched})
        else:
            return render(request, "docs/search.html", {"searched": searched})
    else:
        return render(request, "docs/search.html")


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'docs/edit_comment.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def get_queryset(self):
        """Ensure that only the author or an admin can delete the comment."""
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(author=self.request.user)
    
class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'docs/delete_comment.html'
    context_object_name = 'comment'

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(author=self.request.user)