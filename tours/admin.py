from django.contrib import admin
from .models import Category, Destination, TourPackage, TourImage, TourItinerary, Review

class TourImageInline(admin.TabularInline):
    model = TourImage
    extra = 3


class TourItineraryInline(admin.StackedInline):
    model = TourItinerary
    extra = 3
    fieldsets = (
        (None, {
            'fields': (('day_number', 'title'), 'description', 'activities')
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'best_time_to_visit', 'weather_info', 'featured')
    list_filter = ('featured',)
    list_editable = ('featured',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'attractions')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'category', 'price', 'discount_price', 'available_seats', 'difficulty', 'featured', 'is_active')
    list_filter = ('featured', 'is_active', 'difficulty', 'destination', 'category')
    search_fields = ('title', 'description', 'destination__name')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('price', 'discount_price', 'available_seats', 'featured', 'is_active')
    inlines = [TourImageInline, TourItineraryInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('package', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('comment', 'user__username', 'package__title')
    readonly_fields = ('package', 'user', 'rating', 'comment', 'created_at')
