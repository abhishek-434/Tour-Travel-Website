from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(5, 0, -1)], attrs={
                'class': 'form-select form-glass',
                'required': 'required'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-control form-glass',
                'placeholder': 'Write your review here... How was the hotel, the guides, and the itinerary?',
                'rows': 4,
                'required': 'required'
            }),
        }
