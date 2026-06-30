from django.test import TestCase
from django.contrib.auth.models import User
from tours.models import Category, Destination, TourPackage
from bookings.models import Booking, TravelerDetail
import datetime
from decimal import Decimal

class BookingSystemTestCase(TestCase):
    def setUp(self):
        # Setup category
        self.category = Category.objects.create(
            name="Luxury Escapes", 
            slug="luxury", 
            icon="bi-gem",
            description="Luxury packages"
        )
        
        # Setup destination
        self.destination = Destination.objects.create(
            name="Bali, Indonesia", 
            slug="bali", 
            description="Tropical paradise island",
            attractions="Ubud, Uluwatu",
            best_time_to_visit="April to October",
            weather_info="26°C - 31°C average"
        )
        
        # Setup package
        self.package = TourPackage.objects.create(
            title="Bali Lagoons Escape",
            slug="bali-lagoons-escape",
            destination=self.destination,
            category=self.category,
            price=Decimal('1000.00'),
            duration_days=5,
            available_seats=10,
            included_services="Lodging, breakfasts",
            excluded_services="Airlines flights"
        )
        
        # Setup traveler user
        self.user = User.objects.create_user(username="testtraveler", password="testpassword123")

    def test_booking_creation_and_reference_generation(self):
        # Create a confirmed booking with 2 travelers
        booking = Booking.objects.create(
            user=self.user,
            package=self.package,
            travel_date=datetime.date.today() + datetime.timedelta(days=10),
            number_of_travelers=2,
            total_amount=Decimal('2200.00'), # Price (1000 * 2) + 10% fee (200)
            status='confirmed'
        )
        
        # Verify unique reference auto-generation
        self.assertTrue(booking.booking_reference.startswith("WND-"))
        self.assertEqual(booking.number_of_travelers, 2)
        self.assertEqual(booking.total_amount, Decimal('2200.00'))
        
        # Add traveler profiles
        t1 = TravelerDetail.objects.create(
            booking=booking,
            full_name="John Traveler",
            age=34,
            gender="male"
        )
        t2 = TravelerDetail.objects.create(
            booking=booking,
            full_name="Jane Traveler",
            age=32,
            gender="female"
        )
        
        # Assert database relationships
        self.assertEqual(booking.travelers.count(), 2)
        self.assertIn(t1, booking.travelers.all())
        self.assertIn(t2, booking.travelers.all())
        self.assertEqual(t1.booking, booking)
