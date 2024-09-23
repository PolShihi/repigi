import logging
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import SimpleUploadedFile
from pharmacy_app.models import *

logging.disable(logging.CRITICAL)

class TestSetupMixin:
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        cls.client_group = Group.objects.create(name='Client')
        cls.employee_group = Group.objects.create(name='Employee')

        cls.user1 = User.objects.create_user(
            username='user1', password='Password_1234', email='user1@example.com')
        cls.user1.groups.add(cls.client_group)
        cls.user2 = User.objects.create_user(
            username='user2', password='Password_1234', email='user2@example.com')
        cls.user2.groups.add(cls.client_group)
        cls.employee = User.objects.create_user(
            username='employee', password='Password_1234', email='employee@example.com')
        cls.employee.groups.add(cls.employee_group)

        cls.company_info = CompanyInfo.objects.create(
            text="Company information text")

        cls.supplier = Supplier.objects.create(
            company_name='Supplier1', phone='+375 (29) 000-00-00', address='123 Supplier St')
        cls.category = MedicationCategory.objects.create(
            name='Category1', description='Test Category')

        cls.review = Review.objects.create(
            full_name="John Doe", mark=5, text="Great service!")

        cls.promo = Promo.objects.create(
            promo='PROMO123', is_active=True, discount=1)

        cls.client_instance = Client.objects.create(
            user=cls.user1, age=25, phone='+375 (29) 123-45-67', timezone_info='Europe/Minsk')

        cls.employee_instance = Employee.objects.create(
            user=cls.employee, age=30, phone='+375 (29) 000-00-00', position='Pharmacist', salary=50000.00,
            photo=SimpleUploadedFile(name='employee_image.jpg', content=b'', content_type='image/jpeg'), timezone_info='Europe/Minsk')

        cls.department = PharmacyDepartment.objects.create(
            address='123 Pharmacy St')
        cls.medication = Medication.objects.create(
            code='Med1', name='Test Medication', instruction='Take one daily', description='Test Description',
            cost=10.00, photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            supplier=cls.supplier)

        cls.question = QuestionAnswer.objects.create(
            question="What is the return policy?", answer="30 days return policy.")
        cls.vacancy = Vacancy.objects.create(
            position='Pharmacist', description='Responsible for dispensing medications.', salary=60000.00, requirements='Pharmacy degree')

        cls.order = Order.objects.create(
            medication=cls.medication, client=cls.client_instance, department=cls.department, quantity=2, promo=cls.promo)


class PolicyViewTests(TestSetupMixin, TestCase):
    def test_policy_view_accessible(self):
        response = self.client.get(reverse('pharmacy:policy'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'policy.html')


class InfoViewTests(TestSetupMixin, TestCase):
    def test_info_view_accessible(self):
        response = self.client.get(reverse('pharmacy:info'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'info.html')
        self.assertIn('info', response.context)
        self.assertEqual(response.context['info'], "Company information text")


class LoginViewTests(TestSetupMixin, TestCase):
    def test_login_view_accessible(self):
        response = self.client.get(reverse('pharmacy:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        response = self.client.post(reverse('pharmacy:login'), data={
                                    'username': 'user1', 'password': 'Password_1234'})
        self.assertRedirects(response, reverse('pharmacy:home'))

    def test_login_failure(self):
        response = self.client.post(reverse('pharmacy:login'), data={
                                    'username': 'user1', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(
            response, 'Please enter a correct username and password.')


class RegisterViewTests(TestSetupMixin, TestCase):
    def test_register_view_accessible(self):
        response = self.client.get(reverse('pharmacy:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_success(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'complexpassword123',
            'age': 30,
            'phone': '+375 (29) 111-22-33',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'newuser@example.com',
            'tzname': 'Europe/Minsk'
        }
        response = self.client.post(
            reverse('pharmacy:register'), data=form_data)
        self.assertRedirects(response, reverse('pharmacy:login'))
        new_user = User.objects.get(username='newuser')
        self.assertEqual(new_user.email, 'newuser@example.com')

    def test_register_failure(self):
        form_data = {
            'username': 'newuser',
            'password1': 'complexpassword123',
            'password2': 'differentpassword',
            'age': 30,
            'phone': '+375 (29) 111-22-33',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'newuser@example.com',
            'tzname': 'Europe/Minsk'
        }
        response = self.client.post(
            reverse('pharmacy:register'), data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertContains(response, 'The two password fields didn’t match.')


class LogoutViewTests(TestSetupMixin, TestCase):
    def test_logout_view_accessible(self):
        self.client.login(username='user1', password='Password_1234')
        response = self.client.get(reverse('pharmacy:logout'))
        self.assertRedirects(response, reverse('pharmacy:login'))


class ReviewsViewTests(TestSetupMixin, TestCase):
    def test_reviews_view_accessible(self):
        response = self.client.get(reverse('pharmacy:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reviews.html')
        self.assertIn('reviews', response.context)
        self.assertEqual(len(response.context['reviews']), 1)


class ReviewCreateViewTests(TestSetupMixin, TestCase):
    def test_anonymous_user_cannot_create_review(self):
        response = self.client.get(reverse('pharmacy:review_create'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_review(self):
        self.client.login(username='user1', password='Password_1234')
        response = self.client.get(reverse('pharmacy:review_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_create.html')

    def test_review_creation_form_validation(self):
        self.client.login(username='user1', password='Password_1234')
        response = self.client.post(reverse('pharmacy:review_create'), data={
                                    'text': 'Nice!', 'mark': 5})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 2)


class PromoViewTests(TestSetupMixin, TestCase):
    def test_promo_view_accessible(self):
        response = self.client.get(reverse('pharmacy:promo'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'promo.html')
        self.assertIn('promo_active', response.context)
        self.assertIn('promo_archived', response.context)
        self.assertEqual(len(response.context['promo_active']), 1)


class QuestionsViewTests(TestSetupMixin, TestCase):
    def test_questions_view_accessible(self):
        response = self.client.get(reverse('pharmacy:questions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions.html')
        self.assertIn('questions', response.context)
        self.assertEqual(len(response.context['questions']), 1)


class TimeViewTests(TestSetupMixin, TestCase):
    def test_time_view_accessible(self):
        response = self.client.get(reverse('pharmacy:time'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'time.html')
        self.assertIn('timezones', response.context)
        self.assertIn('now', response.context)


class VacanciesViewTests(TestSetupMixin, TestCase):
    def test_vacancies_view_accessible(self):
        response = self.client.get(reverse('pharmacy:vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vacancies.html')
        self.assertIn('vacancies', response.context)
        self.assertEqual(len(response.context['vacancies']), 1)


class SortSearchViewTests(TestSetupMixin, TestCase):
    def test_anonymous_user_cannot_shop(self):
        response = self.client.get(reverse('pharmacy:shop'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_shop(self):
        self.client.login(username='user1', password='Password_1234')
        response = self.client.get(reverse('pharmacy:shop'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_client.html')
        self.assertIn('medications', response.context)
        self.assertEqual(len(response.context['medications']), 1)


class OrderCreateViewTests(TestSetupMixin, TestCase):
    def test_anonymous_user_cannot_create_order(self):
        response = self.client.get(reverse('pharmacy:shop_order', args=[self.medication.pk]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_create_order(self):
        self.client.login(username='user1', password='Password_1234')
        response = self.client.get(reverse('pharmacy:shop_order', args=[self.medication.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop_make_order.html')

    def test_order_creation_form_validation(self):
        self.client.login(username='user1', password='Password_1234')
        form_data = {
            'medication': self.medication.id,
            'department': self.department.id,
            'quantity': 2,
            'promo': self.promo.id
        }
        response = self.client.post(
            reverse('pharmacy:shop_order', args=[self.medication.pk]), data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.count(), 2)
