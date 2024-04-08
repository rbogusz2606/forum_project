from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.MainView.as_view(), name="MainView"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path('register/', views.sign_up, name='register'),
    path('AddPost/', views.AddPost.as_view(), name='AddPost'),
    path('DeletePost/<int:pk>/', views.DeletePost.as_view(), name='DeletePost'),
    path('UpdatePost/<int:pk>/', views.UpdateView.as_view(), name='UpdatePost'),
    path('MyPosts/<str:username>/', views.MyPosts, name='MyPosts'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


