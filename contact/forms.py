from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-glass', 
                'placeholder': 'Your Full Name',
                'required': 'required'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control form-glass', 
                'placeholder': 'Your Email Address',
                'required': 'required'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control form-glass', 
                'placeholder': 'Phone Number (Optional)'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control form-glass', 
                'placeholder': 'Subject of message',
                'required': 'required'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control form-glass', 
                'placeholder': 'Tell us about your travel plans or query...',
                'rows': 5,
                'required': 'required'
            }),
        }
