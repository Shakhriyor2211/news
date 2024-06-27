from news_app.models import News, Category


def latest_news(request):
    news = News.objects.all().order_by('-published_time')[:8]
    category = Category.objects.all()
    context = {
        "latest_news": news,
        "category_list": category,
    }

    return context




