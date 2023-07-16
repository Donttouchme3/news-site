from django.contrib import admin
from .models import Category, Post


# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'watched', 'is_published', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_editable = ['is_published']
    readonly_fields = ['watched']
    list_filter = ['title', 'category', 'watched', 'created_at']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
