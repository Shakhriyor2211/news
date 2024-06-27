from modeltranslation.translator import TranslationOptions, register

from news_app.models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('value',)