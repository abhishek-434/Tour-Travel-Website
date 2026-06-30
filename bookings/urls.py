from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<slug:slug>/', views.book_package, name='book_package'),
    path('book-details/', views.enter_traveler_details, name='enter_traveler_details'),
    path('checkout/', views.review_checkout, name='review_checkout'),
    path('success/<str:reference>/', views.booking_success, name='booking_success'),
    path('receipt/<str:reference>/', views.booking_detail, name='booking_detail'),
    path('cancel/<str:reference>/', views.cancel_booking, name='cancel_booking'),
]
