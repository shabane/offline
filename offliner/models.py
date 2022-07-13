from django.db import models
from django.contrib.auth.models import User


class Paper(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.TextField(default='')

    def __str__(self) -> str:
        return self.title
