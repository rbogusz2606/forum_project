from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from .models import Article
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, AddPostForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
class MainView(ListView):
    model = Article
    template_name = "docs/main.html"
    context_object_name = "articles"


def loginPage(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user= User.objects.get(username=username)
        except:
            print("Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('MainView')
        else:
            print('Username or password is incorrect')
        
    return render(request, 'docs/login_page.html')

def logoutUser(request):
    logout(request)
    return redirect('MainView')

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('MainView')
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
        messages.error(self.request, "You have to register if you want to add posts.")
        return super().handle_no_permission()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    
class DeletePost(DeleteView):
    model = Article
    success_url = reverse_lazy('MainView')
    template_name = "docs/delete_view.html"

class UpdateView(UpdateView):
    model = Article
    fields = ["topic", "image", "description"]
    success_url = reverse_lazy('MainView')
    template_name = "docs/update_view.html"


def MyPosts(request, username):
    if not request.user.is_authenticated:
        messages.error(request, "If you want to view posts, you have to create account.")
        return redirect('register')
    else:
        user = get_object_or_404(User, username=username)
        posts = Article.objects.filter(author=user)
        return render(request, 'docs/my_posts.html', {'posts': posts})
        
    