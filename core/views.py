from django.shortcuts import render
from .models import FAQ, Testimonial, GalleryImage, WebsiteSetting

# Dynamic imports to prevent boot failures before Phase 3 model declarations
try:
    from tours.models import Destination, TourPackage
except ImportError:
    Destination = None
    TourPackage = None

def home(request):
    settings = WebsiteSetting.get_solo()
    testimonials = Testimonial.objects.filter(featured=True)[:6]
    faqs = FAQ.objects.all()[:5]
    
    featured_destinations = []
    featured_packages = []
    
    if Destination:
        featured_destinations = Destination.objects.filter(featured=True)[:6]
    if TourPackage:
        # Fetch featured active tour packages
        featured_packages = TourPackage.objects.filter(featured=True, is_active=True)[:4]
        
    context = {
        'settings': settings,
        'testimonials': testimonials,
        'faqs': faqs,
        'featured_destinations': featured_destinations,
        'featured_packages': featured_packages,
    }
    return render(request, 'core/home.html', context)


def about(request):
    settings = WebsiteSetting.get_solo()
    testimonials = Testimonial.objects.all()[:4]
    context = {
        'settings': settings,
        'testimonials': testimonials
    }
    return render(request, 'core/about.html', context)


def services(request):
    return render(request, 'core/services.html')


def faqs(request):
    faqs_list = FAQ.objects.all()
    categorized_faqs = {
        'general': faqs_list.filter(category='general'),
        'booking': faqs_list.filter(category='booking'),
        'tours': faqs_list.filter(category='tours'),
        'payments': faqs_list.filter(category='payments'),
    }
    context = {
        'categorized_faqs': categorized_faqs
    }
    return render(request, 'core/faqs.html', context)


def gallery(request):
    images = GalleryImage.objects.all()
    context = {
        'images': images
    }
    return render(request, 'core/gallery.html', context)


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')


def terms_conditions(request):
    return render(request, 'core/terms_conditions.html')


def custom_404_view(request, exception=None):
    return render(request, 'core/404.html', status=404)
