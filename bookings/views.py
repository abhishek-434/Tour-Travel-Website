from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tours.models import TourPackage
from .models import Booking, TravelerDetail
import datetime
from decimal import Decimal

@login_required
def book_package(request, slug):
    package = get_object_or_404(TourPackage, slug=slug, is_active=True)
    
    if package.available_seats <= 0:
        messages.error(request, "This tour package is currently fully booked.")
        return redirect('tours:package_detail', slug=slug)
        
    if request.method == 'POST':
        travel_date_str = request.POST.get('travel_date')
        num_travelers_str = request.POST.get('number_of_travelers')
        special_requests = request.POST.get('special_requests', '')
        
        try:
            travel_date = datetime.datetime.strptime(travel_date_str, '%Y-%m-%d').date()
            num_travelers = int(num_travelers_str)
        except (ValueError, TypeError):
            messages.error(request, "Invalid date or travelers count.")
            return redirect('bookings:book_package', slug=slug)
            
        if travel_date < datetime.date.today():
            messages.error(request, "Travel date cannot be in the past.")
            return redirect('bookings:book_package', slug=slug)
            
        if num_travelers > package.available_seats:
            messages.error(request, f"Only {package.available_seats} seats are available for this package.")
            return redirect('bookings:book_package', slug=slug)
            
        if num_travelers <= 0:
            messages.error(request, "Number of travelers must be at least 1.")
            return redirect('bookings:book_package', slug=slug)
            
        # Store initial details in session
        request.session['booking_init'] = {
            'package_id': package.id,
            'travel_date': travel_date_str,
            'num_travelers': num_travelers,
            'special_requests': special_requests
        }
        return redirect('bookings:enter_traveler_details')
        
    context = {
        'package': package,
        'today': datetime.date.today().strftime('%Y-%m-%d')
    }
    return render(request, 'bookings/book_init.html', context)


@login_required
def enter_traveler_details(request):
    booking_init = request.session.get('booking_init')
    if not booking_init:
        messages.error(request, "Session expired. Please select your package again.")
        return redirect('tours:packages')
        
    package = get_object_or_404(TourPackage, id=booking_init['package_id'])
    num_travelers = booking_init['num_travelers']
    
    if request.method == 'POST':
        travelers_data = []
        is_valid = True
        
        for i in range(1, num_travelers + 1):
            name = request.POST.get(f'name_{i}', '').strip()
            age_str = request.POST.get(f'age_{i}', '').strip()
            gender = request.POST.get(f'gender_{i}', '').strip()
            
            if not name or not age_str or not gender:
                messages.error(request, f"Please fill out all details for Traveler #{i}.")
                is_valid = False
                break
                
            try:
                age = int(age_str)
                if age <= 0:
                    messages.error(request, f"Age for Traveler #{i} must be greater than zero.")
                    is_valid = False
                    break
            except ValueError:
                messages.error(request, f"Invalid age format for Traveler #{i}.")
                is_valid = False
                break
                
            travelers_data.append({
                'full_name': name,
                'age': age,
                'gender': gender
            })
            
        if is_valid:
            # Save travelers details to session
            request.session['booking_travelers'] = travelers_data
            return redirect('bookings:review_checkout')
            
    context = {
        'package': package,
        'num_travelers': num_travelers,
        'range_travelers': range(1, num_travelers + 1)
    }
    return render(request, 'bookings/traveler_details_form.html', context)


@login_required
def review_checkout(request):
    booking_init = request.session.get('booking_init')
    booking_travelers = request.session.get('booking_travelers')
    
    if not booking_init or not booking_travelers:
        messages.error(request, "Session expired. Please restart booking.")
        return redirect('tours:packages')
        
    package = get_object_or_404(TourPackage, id=booking_init['package_id'])
    num_travelers = booking_init['num_travelers']
    
    # Calculate price breakdowns
    unit_price = package.current_price
    subtotal = unit_price * num_travelers
    
    # Local tax calculation (10% standard service fee/VAT)
    tax_rate = Decimal('0.10')
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
    
    if request.method == 'POST':
        # Simulated credit card payments validation
        card_name = request.POST.get('card_name', '').strip()
        card_number = request.POST.get('card_number', '').strip()
        
        if not card_name or not card_number:
            messages.error(request, "Mock card authentication failed. Fill credit details.")
            return redirect('bookings:review_checkout')
            
        # 1. Create main booking
        booking = Booking(
            user=request.user,
            package=package,
            travel_date=datetime.datetime.strptime(booking_init['travel_date'], '%Y-%m-%d').date(),
            number_of_travelers=num_travelers,
            total_amount=total_amount,
            special_requests=booking_init['special_requests'],
            status='confirmed' # Checked & paid mock
        )
        booking.save()
        
        # 2. Create traveler details
        for trav in booking_travelers:
            TravelerDetail.objects.create(
                booking=booking,
                full_name=trav['full_name'],
                age=trav['age'],
                gender=trav['gender']
            )
            
        # 3. Deduct seat availability count
        package.available_seats -= num_travelers
        package.save()
        
        # 4. Wipe session variables
        del request.session['booking_init']
        del request.session['booking_travelers']
        
        messages.success(request, "Booking processed successfully! Tickets issued.")
        return redirect('bookings:booking_success', reference=booking.booking_reference)
        
    context = {
        'package': package,
        'travel_date': booking_init['travel_date'],
        'num_travelers': num_travelers,
        'travelers': booking_travelers,
        'unit_price': unit_price,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_amount': total_amount
    }
    return render(request, 'bookings/checkout_summary.html', context)


@login_required
def booking_success(request, reference):
    booking = get_object_or_404(Booking, booking_reference=reference, user=request.user)
    context = {
        'booking': booking
    }
    return render(request, 'bookings/booking_success.html', context)


@login_required
def booking_detail(request, reference):
    booking = get_object_or_404(Booking, booking_reference=reference, user=request.user)
    
    # Calculate receipt breakdowns
    unit_price = booking.package.current_price
    subtotal = unit_price * booking.number_of_travelers
    tax_amount = booking.total_amount - subtotal
    
    context = {
        'booking': booking,
        'subtotal': subtotal,
        'tax_amount': tax_amount
    }
    return render(request, 'bookings/booking_receipt.html', context)


@login_required
def cancel_booking(request, reference):
    booking = get_object_or_404(Booking, booking_reference=reference, user=request.user)
    
    if booking.status == 'cancelled':
        messages.error(request, "This booking has already been cancelled.")
        return redirect('dashboard:booking_history')
        
    # Cancel the booking
    booking.status = 'cancelled'
    booking.save()
    
    # Return seats back to the package pool
    package = booking.package
    package.available_seats += booking.number_of_travelers
    package.save()
    
    messages.success(request, f"Booking '{booking.booking_reference}' has been cancelled. Refund processing request logged.")
    return redirect('dashboard:booking_history')
