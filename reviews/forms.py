from django import forms
from django.utils.safestring import mark_safe
from .models import Review


class ReviewForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # Star Rating Choices
        rating_choices = [
            (i, mark_safe(
                f"""{i * '<i class="fa fa-star filled-star"></i>'}"""))
            for i in range(1, 6)
        ]

        self.fields['rating'] = forms.ChoiceField(
            choices=rating_choices,
            widget=forms.RadioSelect(attrs={'class': 'filled-star'}),
            label="Rating"
        )

        labels = {
            'headline': mark_safe(
                "Headline <span class='text-muted'>(optional)</span>"),
            'content': mark_safe(
                "Content <span class='text-muted'>(optional)</span>")
        }

        for field_name, label in labels.items():
            if field_name in self.fields:
                self.fields[field_name].label = label

        placeholders = {
            'headline': 'Brief headline for your review',
            'content': 'Write your review here'
        }

        for field_name, placeholder in placeholders.items():
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update(
                    {'placeholder': placeholder})

    class Meta:
        model = Review
        fields = ['rating', 'headline', 'content']
