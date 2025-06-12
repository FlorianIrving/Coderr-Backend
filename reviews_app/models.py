from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ReviewGetPostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)