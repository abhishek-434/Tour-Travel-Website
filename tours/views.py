from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Category, Destination, TourPackage, Review
from .forms import ReviewForm

def destinations(request):
    search_query = request.GET.get('search', '').strip()
    destinations_list = Destination.objects.all()
    
    if search_query:
        destinations_list = destinations_list.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(attractions__icontains=search_query)
        )
        
    paginator = Paginator(destinations_list, 9)
    page_number = request.GET.get('page')
    destinations = paginator.get_page(page_number)
    
    context = {
        'destinations': destinations,
        'search_query': search_query
    }
    return render(request, 'tours/destinations.html', context)


def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    # Fetch active packages belonging to this destination
    packages = destination.packages.filter(is_active=True)
    attractions_list = [a.strip() for a in destination.attractions.split(',') if a.strip()]
    
    context = {
        'destination': destination,
        'packages': packages,
        'attractions_list': attractions_list
    }
    return render(request, 'tours/destination_detail.html', context)


def packages(request):
    packages_list = TourPackage.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Extract query filters
    search_query = request.GET.get('search', '').strip()
    category_slug = request.GET.get('category', '').strip()
    duration_filter = request.GET.get('duration', '').strip()
    difficulty_filter = request.GET.get('difficulty', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    
    if search_query:
        packages_list = packages_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(destination__name__icontains=search_query)
        )
        
    if category_slug:
        packages_list = packages_list.filter(category__slug=category_slug)
        
    if duration_filter:
        try:
            days = int(duration_filter)
            packages_list = packages_list.filter(duration_days__lte=days)
        except ValueError:
            pass
            
    if difficulty_filter:
        packages_list = packages_list.filter(difficulty=difficulty_filter)
        
    if min_price:
        try:
            packages_list = packages_list.filter(price__gte=float(min_price))
        except ValueError:
            pass
            
    if max_price:
        try:
            packages_list = packages_list.filter(price__lte=float(max_price))
        except ValueError:
            pass

    paginator = Paginator(packages_list, 9)
    page_number = request.GET.get('page')
    packages = paginator.get_page(page_number)
    
    context = {
        'packages': packages,
        'categories': categories,
        'filters': {
            'search': search_query,
            'category': category_slug,
            'duration': duration_filter,
            'difficulty': difficulty_filter,
            'min_price': min_price,
            'max_price': max_price
        }
    }
    return render(request, 'tours/packages.html', context)


def package_detail(request, slug):
    package = get_object_or_404(TourPackage, slug=slug)
    images = package.images.all()
    itineraries = package.itineraries.all().order_by('day_number')
    reviews = package.reviews.all().order_by('-created_at')
    
    # Process included and excluded lists
    included_list = [item.strip() for item in package.included_services.split('\n') if item.strip()]
    excluded_list = [item.strip() for item in package.excluded_services.split('\n') if item.strip()]
    
    # Fetch related packages (same destination or same category)
    related_packages = TourPackage.objects.filter(
        is_active=True
    ).filter(
        Q(destination=package.destination) | Q(category=package.category)
    ).exclude(id=package.id)[:3]
    
    # Review form handling
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.info(request, "Please log in to submit a review.")
            return redirect('accounts:login')
            
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.package = package
            review.user = request.user
            review.save()
            messages.success(request, "Thank you! Your review has been published.")
            return redirect('tours:package_detail', slug=slug)
        else:
            messages.error(request, "Failed to submit review. Check form inputs.")
    else:
        review_form = ReviewForm()
        
    context = {
        'package': package,
        'images': images,
        'itineraries': itineraries,
        'reviews': reviews,
        'included_list': included_list,
        'excluded_list': excluded_list,
        'related_packages': related_packages,
        'review_form': review_form
    }
    return render(request, 'tours/package_detail.html', context)
