from django.db import models
from django.contrib.auth.models import User
from pharmacy_proj.common_timezones import COMMON_TIMEZONES
from django.core.validators import MinValueValidator, MaxValueValidator

class MedicationCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Supplier(models.Model):
    company_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.company_name
    
    def get_list_of_orders(self):
        return [order for medication in self.medication_set.all() for order in medication.order_set.all()]

class PharmacyDepartment(models.Model):
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.address
    
    def get_total_revenue(self):
        return sum((order.get_total_cost() for order in self.order_set.all()))

class Medication(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    instruction = models.TextField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    photo = models.ImageField(upload_to='medication_photos')
    categories = models.ManyToManyField(MedicationCategory)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_total_revenue(self):
        return sum((order.get_total_cost() for order in self.order_set.all()))
    
    def get_total_number_of_ordered(self):
        return sum((order.quantity for order in self.order_set.all()))

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20, default='')
    position = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.ImageField(upload_to='employee_photos')
    timezone_info = models.CharField(max_length=32, choices=tuple((el, el) for el in COMMON_TIMEZONES))
    suppliers = models.ManyToManyField(Supplier)

    def __str__(self):
        return self.user.get_full_name()
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    timezone_info = models.CharField(max_length=32, choices=tuple((el, el) for el in COMMON_TIMEZONES))

    def __str__(self):
        return self.user.get_full_name()
    
class CompanyInfo(models.Model):
    text = models.TextField()
    
    def __str__(self):
        return self.text
    
class QuestionAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
class Promo(models.Model):
    promo = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    is_active = models.BooleanField()
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[
            MinValueValidator(0.00),
            MaxValueValidator(1.00),
        ])
    
    def __str__(self):
        return self.promo
    
class Review(models.Model):
    full_name = models.CharField(max_length=50)
    text = models.TextField()
    mark = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ])
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.text
    
class Vacancy(models.Model):
    position = models.CharField(max_length=100)
    description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    requirements = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.position
    
class Order(models.Model):
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(PharmacyDepartment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_of_order = models.DateTimeField(auto_now_add=True)
    promo = models.ForeignKey(Promo, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return str(self.client) + ', ' + str(self.medication)
    
    def get_total_cost(self):
        return round(self.medication.cost * self.quantity * (self.promo.discount if (self.promo is not None and self.promo.is_active) else 1), 2)