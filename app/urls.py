from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="MainView"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.register, name='register'),
    path('AddPost/', views.AddPost.as_view(), name='AddPost'),
    path('DeletePost/<int:pk>/', views.DeletePost.as_view(), name='DeletePost'),
    path('UpdatePost/<int:pk>/', views.UpdatePost.as_view(), name='UpdatePost'),
    path('MyPosts/<str:username>/', views.MyPosts, name='MyPosts'),
    path('post/<int:pk>/', views.ArticleDetailView.as_view(), name='post_detail'),
    path('search/', views.search, name='search'),
    path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete_comment'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


