from django.test import TestCase

# Create your tests here.


from leads.forms import LeadForm

class LeadFormValidationTests(TestCase):
    def test_message_max_length_validation(self):
        long_message = "a" * 3001
        form_data = {
            'name': 'Test User',
            'email': 'user@example.com',
            'preferred_contact': 'email',
            'message': long_message,
        }
        form = LeadForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)
        self.assertIn('Ensure this value has at most 3000 characters', str(form.errors['message']))
