from django.db import models


class Lead(models.Model):
    PREFERRED_CONTACT_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    business_name = models.CharField(max_length=150, blank=True)
    preferred_contact = models.CharField(max_length=20, choices=PREFERRED_CONTACT_CHOICES, default='email')
    message = models.TextField()
    source = models.CharField(max_length=50, default='services_page')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.name} ({self.email})'
