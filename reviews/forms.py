from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        placeholders = {
            'headline': 'Brief headline for your review',
            'content': 'Write your review here'
        }
        
        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({'placeholder': placeholder})

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'content']
