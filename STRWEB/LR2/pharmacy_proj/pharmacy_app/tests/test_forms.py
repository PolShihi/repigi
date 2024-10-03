from django.test import TestCase
from django.contrib.auth.forms import AuthenticationForm
from pharmacy_app.forms import *


class LoginFormTestCase(TestCase):
    def test_form(self):
        form = LoginForm()
        self.assertIsInstance(form, AuthenticationForm)


class RegistrationFormTestCase(TestCase):
    def test_labels_help_texts_initials(self):
        form = RegistrationForm()

        self.assertEqual(form.fields['age'].help_text, '')
        self.assertEqual(form.fields['phone'].help_text,
                         '\'+375 (29) XXX-XX-XX\' form, where \'X\' is digit')
        self.assertEqual(form.fields['phone'].initial, '+375 (29) 000-00-00')

    def test_valid_data(self):
        form = RegistrationForm(data={
            'username': 'user1',
            'password1': 'Password_1234',
            'password2': 'Password_1234',
            'age': 25,
            'phone': '+375 (29) 123-45-67',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'tzname': 'UTC',
        })
        self.assertTrue(form.is_valid())

    def test_invalid_phone(self):
        form = RegistrationForm(data={
            'username': 'user1',
            'password1': 'Password_1234',
            'password2': 'Password_1234',
            'age': 25,
            'phone': '12345',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'tzname': 'UTC',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Only \'+375 (29) XXX-XX-XX\' form allowed, where \'X\' is digit', form.errors['phone'])


class ReviewFormTestCase(TestCase):
    def test_valid_data(self):
        form = ReviewForm(data={'text': 'Great service', 'mark': 5})
        self.assertTrue(form.is_valid())

    def test_invalid_mark(self):
        form = ReviewForm(data={'text': 'Great service', 'mark': 6})
        self.assertFalse(form.is_valid())


class MedicationSortSearchFormTestCase(TestCase):
    def test_valid_data(self):
        form = MedicationSortSearchForm(
            data={'search': 'test', 'sort_by': 'name', 'reverse_sort': True})
        self.assertTrue(form.is_valid())

    def test_valid_search(self):
        form = MedicationSortSearchForm(
            data={'search': 'test', 'sort_by': 'test', 'reverse_sort': True})
        self.assertFalse(form.is_valid())


class MakeOrderFormTestCase(TestCase):
    def setUp(self):
        self.department = PharmacyDepartment.objects.create(
            address='123 Pharmacy St')
        self.promo = Promo.objects.create(
            promo='PROMO1', description='Test Promo', is_active=True, discount=0.10)

    def test_valid_data(self):
        form = MakeOrderForm(
            data={'quantity': 2, 'department': self.department.id, 'promotional_code': 'PROMO1'})
        self.assertTrue(form.is_valid())

    def test_invalid_promotional_code(self):
        form = MakeOrderForm(
            data={'quantity': 2, 'department': self.department.id, 'promotional_code': 'INVALID'})
        self.assertFalse(form.is_valid())
        self.assertIn("Promotional code doesn't exist.",
                      form.errors['promotional_code'])
