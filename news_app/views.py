from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView, View
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin, HitCountDetailView
from unidecode import unidecode

from news_app.forms import ContactForm, CommentsForm
from news_app.models import News, Category
from news_project.permissions import UserIsStaff


class LandingPageView(ListView):
    model = News
    template_name = 'index.html'
    context_object_name = "news"

    # politics =Category.objects.filter(name='politics').first()
    # news = politics.category.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.all()


        context['news'] = self.model.published.all().order_by('-published_time')
        context['politics'] = {
            "list": News.published.all().order_by('-published_time').filter(category__name='politics'),
            "name": category.filter(name='politics').first().value
        }
        context['business'] = {
            "list": News.published.all().order_by('-published_time').filter(category__name='business'),
            "name": category.filter(name='business').first().value
        }
        context['technology'] = {
            "list": News.published.all().order_by('-published_time').filter(category__name='technology'),
            "name": category.filter(name='technology').first().value
        }
        context['sport'] = {
            "list": News.published.all().order_by('-published_time').filter(category__name='sport'),
            "name": category.filter(name='sport').first().value
        }
        context['tourism'] = {
            "list": News.published.all().order_by('-published_time').filter(category__name='tourism'),
            "name": category.filter(name='tourism').first().value
        }
        return context

# @user_passes_test
# def landingPageView(request):
#     news = News.published.all().order_by('-published_time')
#     category = Category.objects.all()
#     business = News.published.all().order_by('-published_time').filter(category__name="Business")
#
#     context = {
#         "news": news,
#         "category": category,
#         "business": business
#     }
#     return render(request, 'index.html', context)

# @user_passes_test
# def contactPageView(request):
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse('<h3>Success!</h3>')
#
#     context = {
#         form: form
#     }
#     return render(request, 'contact.html', context)


class ContactPageView(TemplateView):
    template_name = 'contact.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': ContactForm(),

        }
        return render(request, 'contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return redirect('landing_page')

        context = {
            'form': form,
        }

        return render(request, 'contact.html', context)


class SinglePageView(TemplateView):
    template_name = 'single_page.html'


class NotFoundPageView(TemplateView):
    template_name = '404.html'


class CategoriesPageView(DetailView):
    model = Category
    template_name = 'category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get("pk")
        context['category_news'] = News.published.filter(category=category_id)
        context['category_title'] = Category.objects.filter(id=category_id).first().name.capitalize()
        return context


class DetailsPageView(HitCountDetailView):
    def handle_request(self, slug):
        news = get_object_or_404(News, slug=slug, status=News.Status.Published)
        return news, news.comments.filter(active=True)

    def get(self, request, **kwargs):
        news, comments = self.handle_request(kwargs['slug'])
        context = {
            "news": news,
            'comments': comments,
            'comment_form': CommentsForm()
        }
        hit_count = get_hitcount_model().objects.get_for_object(news)
        hits = hit_count.hits
        hitcontext = context['hitcount'] = {'pk': hit_count.pk}
        hit_count_respones = HitCountMixin.hit_count(request, hit_count)

        if hit_count_respones.hit_counted:
            hits = hits + 1
            hitcontext['hit_counted'] = hit_count_respones.hit_counted
            hitcontext['hit_message'] = hit_count_respones.hit_message
            hitcontext['total_hits'] = hits

        return render(request, 'detail.html', context)

    def post(self, request, **kwargs):
        news, comments = self.handle_request(kwargs['slug'])
        comment_form = CommentsForm(data=request.POST)
        comments = news.comments.filter(active=True)
        context = {
            "news": news,
            'comments': comments,
            'comment_form': CommentsForm()
        }
        if comment_form.is_valid():
            new_form = comment_form.save(commit=False)
            new_form.user = request.user
            new_form.news = news
            new_form.save()
            return  redirect(request.path)
        return render(request, 'detail.html', context)




def detailsPageView(request, **kwargs):
    slug = kwargs['slug']
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    comments = news.comments.filter(active=True)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_respones = HitCountMixin.hit_count(request, hit_count)

    if hit_count_respones.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_respones.hit_counted
        hitcontext['hit_message'] = hit_count_respones.hit_message
        hitcontext['total_hits'] = hits

    if request.method == "POST":
        comments_form = CommentsForm(data=request.POST)
        if comments_form.is_valid():
            news_form = comments_form.save(commit=False)
            news_form.user = request.user
            news_form.news = news
            news_form.save()
            return redirect(request.path)
        context = {
            "news": news,
            'comments': comments,
            'comment_form': comments_form
        }

        return render(request, 'detail.html', context)
    else:
        context['news'] = news
        context['comments'] = comments
        context['comment_form'] = CommentsForm()


    return render(request, 'detail.html', context)


class DashboardPageView(UserIsStaff, ListView):
    model = News
    template_name = 'staff/index.html'
    context_object_name = "news"


class CreateNewsPageView(UserIsStaff, CreateView):
    model = News
    template_name = 'staff/create_news.html'
    fields = ("title_uz", "title_ru", "title_en", "body_uz", "body_ru", "body_en", "image", "category", "status")

    success_url = reverse_lazy("dashboard_page")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context




class UpdateNewsPageView(UserIsStaff, UpdateView):
    model = News
    template_name = "staff/update_news.html"
    fields = ("title_uz", "title_ru", "title_en", "body_uz", "body_ru", "body_en", "image", "category", "status")
    success_url = reverse_lazy("dashboard_page")

    def form_valid(self, form):
        title = form.cleaned_data.get('title_en') or form.cleaned_data.get('title_uz') or form.cleaned_data.get(
            'title_ru')
        form.instance.slug = slugify(unidecode(title))
        return super().form_valid(form)


class DeleteNewsPageView(UserIsStaff, UserPassesTestMixin, DeleteView):
    model = News
    template_name = "staff/delete_news.html"
    success_url = reverse_lazy("dashboard_page")

    # def test_func(self):
    #     return  self.request.user.is_staff or self.request.user.is_superuser



class SearchPageView(ListView):
    model = News
    template_name = 'search.html'
    context_object_name = 'news'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.all().filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(category__name__icontains=query))
