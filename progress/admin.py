from django.contrib import admin
from progress.models import Posts


# Register your models here.
@admin.register(Posts)
class Posts(admin.ModelAdmin):
    list_display = ('website_page', 'post_title')
    list_display_links = ('post_title',)
