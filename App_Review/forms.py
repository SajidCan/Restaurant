from django import forms
from App_Review.models import Review_Cart, Review

class ReviewRateForm(forms.ModelForm):
    class Meta:
        model=Review_Cart
        fields=('rating','review_food')
class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=('review_order',)
