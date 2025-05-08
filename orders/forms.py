from django import forms
from stores.models import ReviewRating

class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        labels = {
            'subject': 'Шолу тақырыбы',
            'review': 'Сіздің пікіріңіз',
            'rating': 'Сіздің бағаңыз',
        }
        widgets = {
            'review': forms.Textarea(attrs={'rows': 3}),
        }
