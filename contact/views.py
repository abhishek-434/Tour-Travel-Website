from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import ContactMessage, NewsletterSubscriber
from .forms import ContactForm
from core.models import WebsiteSetting
import json

def contact(request):
    settings = WebsiteSetting.get_solo()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                "Your inquiry has been logged! A Wanderlust travel specialist will review it and contact you soon."
            )
            return redirect('contact:contact')
        else:
            messages.error(request, "Failed to submit message. Please correct the fields below.")
    else:
        form = ContactForm()
        
    context = {
        'form': form,
        'settings': settings
    }
    return render(request, 'contact/contact.html', context)


def newsletter_signup(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)
        
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'success': False, 'message': 'Invalid form payload.'}, status=400)
        
    if not email:
        return JsonResponse({'success': False, 'message': 'Email address is required.'}, status=400)
        
    subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
    
    if created:
        return JsonResponse({
            'success': True, 
            'message': 'Successfully subscribed to the Wanderlust newsletter!'
        })
    else:
        return JsonResponse({
            'success': False, 
            'message': 'This email address is already subscribed.'
        })
