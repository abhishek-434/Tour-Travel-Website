from django.contrib import admin
from .models import Booking, TravelerDetail

class TravelerDetailInline(admin.TabularInline):
    model = TravelerDetail
    extra = 0
    readonly_fields = ('full_name', 'age', 'gender')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'user', 'package', 'travel_date', 'number_of_travelers', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'travel_date', 'created_at')
    search_fields = ('booking_reference', 'user__username', 'package__title', 'user__email')
    readonly_fields = ('booking_reference', 'user', 'package', 'total_amount', 'created_at')
    list_editable = ('status',)
    inlines = [TravelerDetailInline]
