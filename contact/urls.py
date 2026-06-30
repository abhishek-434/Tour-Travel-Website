from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name='contact'),
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]
