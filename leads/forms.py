from django import forms


class LeadForm(forms.Form):
    name = forms.CharField(
        label='Name',
        max_length=120,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
    )
    phone = forms.CharField(
        label='Phone',
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone (optional)'}),
    )
    business_name = forms.CharField(
        label='Business / Project',
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business or project name'}),
    )
    preferred_contact = forms.ChoiceField(
        label='Preferred Contact',
        choices=[('email', 'Email'), ('phone', 'Phone')],
        initial='email',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    message = forms.CharField(
        label='Project Details',
        max_length=3000,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us what you are building.'}),
    )
    website = forms.CharField(label='Website', required=False, widget=forms.HiddenInput(attrs={'class': 'honeypot'}))
