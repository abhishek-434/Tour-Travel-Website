from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="bi-compass", help_text="Bootstrap Icon class, e.g. bi-compass")
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Destination(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hero_image = models.ImageField(upload_to='destinations/')
    description = models.TextField()
    attractions = models.TextField(help_text="Key tourist attractions (comma-separated or HTML/markdown)")
    best_time_to_visit = models.CharField(max_length=150, help_text="E.g., October to April")
    weather_info = models.CharField(max_length=200, help_text="E.g., 20°C - 30°C Average")
    featured = models.BooleanField(default=False, help_text="Show this destination on the home page spotlight")
    nearby_destinations = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tours:destination_detail', kwargs={'slug': self.slug})


class TourPackage(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('challenging', 'Challenging'),
        ('extreme', 'Extreme'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='packages')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='packages')
    cover_image = models.ImageField(upload_to='packages/')
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0)])
    duration_days = models.PositiveIntegerField(default=1)
    duration_nights = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField(default=10)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    best_season = models.CharField(max_length=100, help_text="E.g., Winter / Summer")
    
    included_services = models.TextField(help_text="Items included, separated by newlines")
    excluded_services = models.TextField(help_text="Items excluded, separated by newlines")
    
    map_iframe = models.TextField(blank=True, help_text="Google Maps iframe link only (src attribute value)")
    featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tours:package_detail', kwargs={'slug': self.slug})

    @property
    def current_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def has_discount(self):
        return bool(self.discount_price and self.discount_price < self.price)

    @property
    def discount_amount(self):
        if self.has_discount:
            return self.price - self.discount_price
        return 0

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0.0
        return sum([r.rating for r in reviews]) / len(reviews)


class TourImage(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='packages/gallery/')
    alt_text = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return f"Gallery Image for {self.package.title}"


class TourItinerary(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    activities = models.TextField(blank=True, help_text="Highlight activities for this day (newline separated)")

    class Meta:
        ordering = ['day_number']
        unique_together = ('package', 'day_number')

    @property
    def activities_list(self):
        if self.activities:
            return [a.strip() for a in self.activities.split(',') if a.strip()]
        return []

    def __str__(self):
        return f"Day {self.day_number}: {self.title} ({self.package.title})"


class Review(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tours_reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.package.title} - {self.rating}★"
