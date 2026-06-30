from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserUpdateForm, UserProfileForm
from tours.models import TourPackage

@login_required
def profile(request):
    user = request.user
    profile = user.profile
    
    # Lazy fetch of bookings. We'll implement bookings FK to User soon.
    # If no bookings exist yet or relation is missing, fallback to empty list
    try:
        bookings = user.bookings.all().order_by('-created_at')[:3]
        total_bookings = user.bookings.count()
        active_bookings = user.bookings.filter(status__in=['pending', 'confirmed']).count()
    except AttributeError:
        bookings = []
        total_bookings = 0
        active_bookings = 0
        
    saved_packages = profile.favorite_packages.all()[:3]
    
    context = {
        'profile': profile,
        'bookings': bookings,
        'total_bookings': total_bookings,
        'active_bookings': active_bookings,
        'saved_packages': saved_packages
    }
    return render(request, 'dashboard/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your travel profile has been updated successfully!")
            return redirect('dashboard:profile')
        else:
            messages.error(request, "Failed to update profile. Please check the inputs below.")
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'dashboard/edit_profile.html', context)


@login_required
def booking_history(request):
    user = request.user
    try:
        bookings = user.bookings.all().order_by('-created_at')
    except AttributeError:
        bookings = []
        
    context = {
        'bookings': bookings
    }
    return render(request, 'dashboard/booking_history.html', context)


@login_required
def saved_packages(request):
    saved_list = request.user.profile.favorite_packages.all()
    context = {
        'saved_list': saved_list
    }
    return render(request, 'dashboard/saved_packages.html', context)


@login_required
def toggle_favorite(request, slug):
    package = get_object_or_404(TourPackage, slug=slug)
    profile = request.user.profile
    
    if profile.favorite_packages.filter(id=package.id).exists():
        profile.favorite_packages.remove(package)
        messages.success(request, f"Removed '{package.title}' from your saved journeys list.")
    else:
        profile.favorite_packages.add(package)
        messages.success(request, f"Saved '{package.title}' to your saved journeys list!")
        
    # Redirect back to referring page or package detail page
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('tours:package_detail', slug=slug)
