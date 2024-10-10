from django.contrib import admin
from scraper.models import Website, Property
from scraper.selenium.extract_cbc_data import CBCScraper


# Acción personalizada para ejecutar el scraper
def scrape_selected_websites(model_admin, request, queryset):
    chromedriver_path = '/app/scraper/selenium/bin/chromedriver-linux64/chromedriver'

    for website in queryset:
        scraper = CBCScraper(website.url, chromedriver_path, request, website)
        scraper.start()

    model_admin.message_user(request, "Scraping for selected websites completed.")


scrape_selected_websites.short_description = "Scrape selected websites"


# Register your models here.
@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'site_name', 'url')
    list_display_links = ('site_name',)
    actions = [scrape_selected_websites]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'property_name', 'property_price', 'property_address', 'property_url', 'website_name')
    list_display_links = ('property_name',)
