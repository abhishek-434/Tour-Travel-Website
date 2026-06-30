from django.contrib import admin
from .models import WebsiteSetting, FAQ, Testimonial, GalleryImage

@admin.register(WebsiteSetting)
class WebsiteSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'contact_phone', 'updated_at')
    
    def has_add_permission(self, request):
        # Exclude ability to add multiple setting rows for Singleton
        if WebsiteSetting.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of Singleton settings row
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('order',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_designation', 'rating', 'featured', 'created_at')
    list_filter = ('rating', 'featured', 'created_at')
    search_fields = ('client_name', 'testimonial_text')
    list_editable = ('featured',)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'tourist_name', 'location', 'created_at')
    search_fields = ('caption', 'tourist_name', 'location')
