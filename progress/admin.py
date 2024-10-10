from django.contrib import admin
from progress.models import Posts


# Register your models here.
@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'website', 'date')
    list_display_links = ('post_title',)
