from django.conf import settings

def my_site_url(request):
    return {
        "SITE_URL": settings.SITE_URL
    }
