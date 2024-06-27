from django.contrib import admin

from .models import News, Category, Contact, Comments


# @admin.register(Category)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'value']

# @admin.register(News)

class NewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'title', 'slug', 'published_time', 'status']
    list_filter = ['published_time', 'created_time', 'updated_time', 'status']
    exclude = ('slug',)
    date_hierarchy = 'published_time'
    search_fields = ['title', 'body']
    ordering = ['published_time', 'status']
    list_editable = ('status',)




class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'email']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'news', 'body','active']
    list_filter = ['active', 'user', 'news']
    search_fields = ['user', 'body']
    actions = ['disable_comment', 'enable_comment']
    def disable_comment(self, request, queryset):
        queryset.update(active=False)

    def enable_comment(self, request, queryset):
        queryset.update(active=True)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
