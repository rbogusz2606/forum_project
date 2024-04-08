from django.db import models
from django.contrib.auth.models import User






class Article(models.Model):
    topic = models.CharField(max_length=200)
    image = models.ImageField(upload_to="photos/images/", default=None, null=True, blank=True)
    description = models.TextField(max_length=10000, null=False, blank=False)
    date= models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self) -> str:
        return self.topic
   
