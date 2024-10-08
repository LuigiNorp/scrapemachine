from django.contrib import admin
from scraper.models import Website, Property


# Register your models here.
@admin.register(Website)
class Website(admin.ModelAdmin):
    list_display = ('id', 'site_name', 'url')
    list_display_links = ('site_name',)


@admin.register(Property)
class Property(admin.ModelAdmin):
    list_display = ('id', 'post', 'property_name', 'property_price', 'property_address', 'property_url', 'website_name')
    list_display_links = ('property_name',)
