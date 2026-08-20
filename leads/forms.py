from django import forms


class LeadForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=120,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Your email'}),
    )
    phone = forms.CharField(
        label='Phone',
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Phone (optional)'}),
    )
    business_name = forms.CharField(
        label='Business / Project',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Business or project name'}),
    )
    preferred_contact = forms.ChoiceField(
        label='Preferred contact',
        choices=[('email', 'Email'), ('phone', 'Phone')],
        initial='email',
        widget=forms.Select(),
    )
    message = forms.CharField(
        label='Project details',
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Tell us what you are building.'}),
    )
    website = forms.CharField(label='Website', required=False, widget=forms.HiddenInput())
