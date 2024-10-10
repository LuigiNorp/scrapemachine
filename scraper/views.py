from django.shortcuts import redirect
from django.shortcuts import redirect, render


# Create your views here.

def redirect_to_website_admin(request):
    return redirect('/admin/scraper/website/')
