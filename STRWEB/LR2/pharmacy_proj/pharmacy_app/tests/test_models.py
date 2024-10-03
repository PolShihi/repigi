from django.test import TestCase
from pharmacy_app.models import *
import decimal
from django.core.files.uploadedfile import SimpleUploadedFile


class MedicationCategoryTestCase(TestCase):
    def setUp(self):
        self.category = MedicationCategory.objects.create(
            name='Category1', description='Test Category')

    def test_str(self):
        self.assertEqual(str(self.category), 'Category1')

    def test_field_names(self):
        self.assertEqual(self.category._meta.get_field(
            'name').verbose_name, 'name')
        self.assertEqual(self.category._meta.get_field(
            'description').verbose_name, 'description')


class SupplierTestCase(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            company_name='Supplier1', phone='+375 (29) 000-00-00', address='123 Supplier St')

    def test_str(self):
        self.assertEqual(str(self.supplier), 'Supplier1')

    def test_field_names(self):
        self.assertEqual(self.supplier._meta.get_field(
            'company_name').verbose_name, 'company name')
        self.assertEqual(self.supplier._meta.get_field(
            'phone').verbose_name, 'phone')
        self.assertEqual(self.supplier._meta.get_field(
            'address').verbose_name, 'address')

    def test_get_list_of_orders(self):
        self.assertEqual(self.supplier.get_list_of_orders(), [])


class PharmacyDepartmentTestCase(TestCase):
    def setUp(self):
        self.department = PharmacyDepartment.objects.create(
            address='123 Pharmacy St')

    def test_str(self):
        self.assertEqual(str(self.department), '123 Pharmacy St')

    def test_field_names(self):
        self.assertEqual(self.department._meta.get_field(
            'address').verbose_name, 'address')

    def test_get_total_revenue(self):
        self.assertEqual(self.department.get_total_revenue(), 0)


class MedicationTestCase(TestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            company_name='Supplier1', phone='+375 (29) 000-00-00', address='123 Supplier St')
        self.category = MedicationCategory.objects.create(
            name='Category1', description='Test Category')
        self.medication = Medication.objects.create(
            code='MED123', name='Test Medication', instruction='Take one daily', description='Test Description',
            cost=10.00, photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            supplier=self.supplier
        )
        self.medication.categories.add(self.category)

    def test_str(self):
        self.assertEqual(str(self.medication), 'Test Medication')

    def test_field_names(self):
        self.assertEqual(self.medication._meta.get_field(
            'code').verbose_name, 'code')
        self.assertEqual(self.medication._meta.get_field(
            'name').verbose_name, 'name')
        self.assertEqual(self.medication._meta.get_field(
            'instruction').verbose_name, 'instruction')
        self.assertEqual(self.medication._meta.get_field(
            'description').verbose_name, 'description')
        self.assertEqual(self.medication._meta.get_field(
            'cost').verbose_name, 'cost')
        self.assertEqual(self.medication._meta.get_field(
            'photo').verbose_name, 'photo')
        self.assertEqual(self.medication._meta.get_field(
            'categories').verbose_name, 'categories')
        self.assertEqual(self.medication._meta.get_field(
            'supplier').verbose_name, 'supplier')
        self.assertEqual(self.medication._meta.get_field(
            'date_created').verbose_name, 'date created')

    def test_get_total_revenue(self):
        self.assertEqual(self.medication.get_total_revenue(), 0)

    def test_get_total_number_of_ordered(self):
        self.assertEqual(self.medication.get_total_number_of_ordered(), 0)


class EmployeeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='employee1', password='password', first_name='Employee', last_name='One')
        self.supplier = Supplier.objects.create(
            company_name='Supplier1', phone='+375 (29) 000-00-00', address='123 Supplier St')
        self.employee = Employee.objects.create(
            user=self.user, age=30, phone='+375 (29) 000-00-00', position='Pharmacist', salary=50000.00,
            photo=SimpleUploadedFile(name='employee_image.jpg', content=b'', content_type='image/jpeg'), timezone_info='UTC'
        )
        self.employee.suppliers.add(self.supplier)

    def test_str(self):
        self.assertEqual(str(self.employee), 'Employee One')

    def test_field_names(self):
        self.assertEqual(self.employee._meta.get_field(
            'user').verbose_name, 'user')
        self.assertEqual(self.employee._meta.get_field(
            'age').verbose_name, 'age')
        self.assertEqual(self.employee._meta.get_field(
            'phone').verbose_name, 'phone')
        self.assertEqual(self.employee._meta.get_field(
            'position').verbose_name, 'position')
        self.assertEqual(self.employee._meta.get_field(
            'salary').verbose_name, 'salary')
        self.assertEqual(self.employee._meta.get_field(
            'photo').verbose_name, 'photo')
        self.assertEqual(self.employee._meta.get_field(
            'timezone_info').verbose_name, 'timezone info')
        self.assertEqual(self.employee._meta.get_field(
            'suppliers').verbose_name, 'suppliers')


class ClientTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='client1', password='password', first_name='Client', last_name='One')
        self.client = Client.objects.create(
            user=self.user, age=30, phone='+375 (29) 000-00-00', timezone_info='UTC')

    def test_str(self):
        self.assertEqual(str(self.client), 'Client One')

    def test_field_names(self):
        self.assertEqual(self.client._meta.get_field(
            'user').verbose_name, 'user')
        self.assertEqual(self.client._meta.get_field(
            'age').verbose_name, 'age')
        self.assertEqual(self.client._meta.get_field(
            'phone').verbose_name, 'phone')
        self.assertEqual(self.client._meta.get_field(
            'timezone_info').verbose_name, 'timezone info')


class CompanyInfoTestCase(TestCase):
    def setUp(self):
        self.company_info = CompanyInfo.objects.create(
            text='Welcome to our pharmacy')

    def test_str(self):
        self.assertEqual(str(self.company_info), 'Welcome to our pharmacy')

    def test_field_names(self):
        self.assertEqual(self.company_info._meta.get_field(
            'text').verbose_name, 'text')


class QuestionAnswerTestCase(TestCase):
    def setUp(self):
        self.qa = QuestionAnswer.objects.create(
            question='What is the return policy?', answer='30 days return policy')

    def test_str(self):
        self.assertEqual(str(self.qa), 'What is the return policy?')

    def test_field_names(self):
        self.assertEqual(self.qa._meta.get_field(
            'question').verbose_name, 'question')
        self.assertEqual(self.qa._meta.get_field(
            'answer').verbose_name, 'answer')
        self.assertEqual(self.qa._meta.get_field(
            'date_added').verbose_name, 'date added')


class PromoTestCase(TestCase):
    def setUp(self):
        self.promo = Promo.objects.create(
            promo='PROMO1', description='Test Promo', is_active=True, discount=decimal.Decimal('0.10'))

    def test_str(self):
        self.assertEqual(str(self.promo), 'PROMO1')

    def test_field_names(self):
        self.assertEqual(self.promo._meta.get_field(
            'promo').verbose_name, 'promo')
        self.assertEqual(self.promo._meta.get_field(
            'description').verbose_name, 'description')
        self.assertEqual(self.promo._meta.get_field(
            'is_active').verbose_name, 'is active')
        self.assertEqual(self.promo._meta.get_field(
            'discount').verbose_name, 'discount')


class ReviewTestCase(TestCase):
    def setUp(self):
        self.review = Review.objects.create(
            full_name='John Doe', text='Great service', mark=5)

    def test_str(self):
        self.assertEqual(str(self.review), 'Great service')

    def test_field_names(self):
        self.assertEqual(self.review._meta.get_field(
            'full_name').verbose_name, 'full name')
        self.assertEqual(self.review._meta.get_field(
            'text').verbose_name, 'text')
        self.assertEqual(self.review._meta.get_field(
            'mark').verbose_name, 'mark')
        self.assertEqual(self.review._meta.get_field(
            'date_added').verbose_name, 'date added')


class VacancyTestCase(TestCase):
    def setUp(self):
        self.vacancy = Vacancy.objects.create(
            position='Pharmacist', description='Pharmacist job', salary=60000.00, requirements='Pharmacy degree')

    def test_str(self):
        self.assertEqual(str(self.vacancy), 'Pharmacist')

    def test_field_names(self):
        self.assertEqual(self.vacancy._meta.get_field(
            'position').verbose_name, 'position')
        self.assertEqual(self.vacancy._meta.get_field(
            'description').verbose_name, 'description')
        self.assertEqual(self.vacancy._meta.get_field(
            'salary').verbose_name, 'salary')
        self.assertEqual(self.vacancy._meta.get_field(
            'requirements').verbose_name, 'requirements')
        self.assertEqual(self.vacancy._meta.get_field(
            'posted_date').verbose_name, 'posted date')


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='client1', password='password', first_name='Client', last_name='One')
        self.supplier = Supplier.objects.create(
            company_name='Supplier1', phone='+375 (29) 000-00-00', address='123 Supplier St')
        self.department = PharmacyDepartment.objects.create(
            address='123 Pharmacy St')
        self.promo = Promo.objects.create(
            promo='PROMO1', description='Test Promo', is_active=True, discount=decimal.Decimal('0.10'))
        self.medication = Medication.objects.create(
            code='MED123', name='Test Medication', instruction='Take one daily', description='Test Description',
            cost=decimal.Decimal('10.00'), photo=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            supplier=self.supplier
        )
        self.client = Client.objects.create(
            user=self.user, age=30, phone='+375 (29) 000-00-00', timezone_info='UTC')
        self.order = Order.objects.create(medication=self.medication, client=self.client, department=self.department,
                                          quantity=2, promo=self.promo)

    def test_str(self):
        self.assertEqual(str(self.order), 'Client One, Test Medication')

    def test_field_names(self):
        self.assertEqual(self.order._meta.get_field(
            'medication').verbose_name, 'medication')
        self.assertEqual(self.order._meta.get_field(
            'client').verbose_name, 'client')
        self.assertEqual(self.order._meta.get_field(
            'department').verbose_name, 'department')
        self.assertEqual(self.order._meta.get_field(
            'quantity').verbose_name, 'quantity')
        self.assertEqual(self.order._meta.get_field(
            'date_of_order').verbose_name, 'date of order')
        self.assertEqual(self.order._meta.get_field(
            'promo').verbose_name, 'promo')

    def test_get_total_cost(self):
        self.assertEqual(self.order.get_total_cost(),
                         decimal.Decimal('2.00'))  # 2 * 10 * 0.1 discount
