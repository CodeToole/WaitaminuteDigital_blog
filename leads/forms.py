from django import forms


class LeadForm(forms.Form):
    name = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Your name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your email'}))
    phone = forms.CharField(max_length=40, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone (optional)'}))
    business_name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Business or project name'}))
    preferred_contact = forms.ChoiceField(
        choices=[('email', 'Email'), ('phone', 'Phone')],
        initial='email',
        widget=forms.Select(),
    )
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us what you are building.'}))
    website = forms.CharField(required=False, widget=forms.HiddenInput())
