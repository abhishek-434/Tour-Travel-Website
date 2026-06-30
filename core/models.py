from django.db import models

class WebsiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default="Wanderlust")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, help_text="Upload custom site logo")
    contact_email = models.EmailField(default="info@wanderlust.com")
    contact_phone = models.CharField(max_length=20, default="+1 (234) 567-890")
    address = models.TextField(default="123 Luxury Travel Way, Wander City, WC 54321")
    google_maps_embed_url = models.TextField(
        blank=True, 
        help_text="Provide Google Maps iframe src URL. E.g. https://www.google.com/maps/embed?pb=..."
    )
    facebook_url = models.URLField(blank=True, default="https://facebook.com")
    instagram_url = models.URLField(blank=True, default="https://instagram.com")
    twitter_url = models.URLField(blank=True, default="https://twitter.com")
    youtube_url = models.URLField(blank=True, default="https://youtube.com")
    about_summary = models.TextField(
        default="Wanderlust is a premier travel boutique designing bespoke journeys across the globe. We elevate travel experiences with curated destinations, luxury lodgings, and meticulous tour management."
    )
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        super(WebsiteSetting, self).save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"{self.site_name} Website Settings"

    class Meta:
        verbose_name = "Website Setting"
        verbose_name_plural = "Website Settings"


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'General Query'),
        ('booking', 'Booking & Cancellations'),
        ('tours', 'Tour Packages & Customization'),
        ('payments', 'Payments & Invoicing'),
    ]
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=25, choices=CATEGORY_CHOICES, default='general')
    order = models.IntegerField(default=0, help_text="Order in list display")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'order', '-created_at']

    def __str__(self):
        return f"{self.get_category_display()} - {self.question}"


class Testimonial(models.Model):
    client_name = models.CharField(max_length=100)
    client_designation = models.CharField(max_length=100, blank=True, help_text="E.g., Wanderer, Travel Blogger")
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    testimonial_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    featured = models.BooleanField(default=True, help_text="Show on the home page testimonials list")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.client_name} ({self.rating} Stars)"


class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200)
    tourist_name = models.CharField(max_length=100, blank=True, help_text="Name of the tourist (optional)")
    location = models.CharField(max_length=100, blank=True, help_text="Location where it was shot (optional)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.caption
