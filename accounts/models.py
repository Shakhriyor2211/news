from django.contrib.auth.models import User
from django.db import models

from news_app.models import News


class Profile(models.Model):
    photo = models.ImageField(upload_to='users/', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} profile"

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"





