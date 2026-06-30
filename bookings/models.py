from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey('tours.TourPackage', on_delete=models.CASCADE, related_name='bookings')
    travel_date = models.DateField()
    number_of_travelers = models.PositiveIntegerField(default=1)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            date_str = datetime.date.today().strftime('%Y%m')
            # Generate a unique 4-character suffix
            unique_suffix = uuid.uuid4().hex[:4].upper()
            self.booking_reference = f"WND-{date_str}-{unique_suffix}"
            
        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.booking_reference} - {self.package.title} ({self.user.username})"


class TravelerDetail(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='travelers')
    full_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.full_name} (Guest on {self.booking.booking_reference})"
