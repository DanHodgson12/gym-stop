from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating and managing user profile information.
    """

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Initialize the form, add placeholders and CSS classes,
        remove auto-generated labels, and set autofocus on the first field.
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
            'is_subscribed_to_newsletter': 'Subscribed to Marketing Emails?',
        }

        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                widget_attrs = self.fields[field].widget.attrs
                widget_attrs['placeholder'] = placeholder
                widget_attrs['class'] = 'border-black profile-form-input'
            else:
                self.fields[field].widget.attrs['class'] = 'border-black'

            if field == 'is_subscribed_to_newsletter':
                self.fields[field].label = 'Subscribed to Marketing Emails?'
            else:
                self.fields[field].label = False
