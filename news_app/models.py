from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from unidecode import unidecode


# class CustomUser(AbstractUser):
#     is_admin = models.BooleanField(default=False)
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=News.Status.Published)


class Category(models.Model):
    name = models.CharField(max_length=250)
    value = models.CharField(max_length=250, null=True, blank=True)
    def get_absolute_url(self):
        return reverse('category_page', kwargs={'pk': self.id, 'slug': self.name})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class News(models.Model):
    class Status(models.TextChoices):
        Draft = 'DF', 'Draft'
        Published = 'Pb', 'Published'

    title = models.CharField(max_length=250)
    body = models.CharField(max_length=250)
    image = models.ImageField(upload_to='news/images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    published_time = models.DateTimeField(default=timezone.now)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.Draft)
    slug = models.SlugField(max_length=250, unique=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ['-published_time']
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        date = self.created_time
        y = date.strftime("%Y")
        m = date.strftime("%m")
        d = date.strftime("%d")
        return reverse('detail_page', kwargs={'year': y, 'month': m, 'day': d, 'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField()

    class Meta:
        verbose_name = 'Request'
        verbose_name_plural = 'Requests'

    def __str__(self):
        return self.name


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Comment {self.id} by {self.user}"

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        ordering = ['created_time']
