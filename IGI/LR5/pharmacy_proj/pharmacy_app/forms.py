from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from pharmacy_proj.common_timezones import COMMON_TIMEZONES
from .models import *


class LoginForm(AuthenticationForm):
    """
A form for authenticating users by their username and password.

Inherits from Django's built-in AuthenticationForm class.

Attributes:
    None
"""
    pass

class RegistrationForm(UserCreationForm):
    """
A form that extends UserCreationForm to handle user registration with additional fields like age, phone number, first name, last name, email, and timezone selection.

Attributes:
    age (forms.IntegerField): Field to capture user's age with validation for minimum and maximum values.
    phone (forms.CharField): Field to capture user's phone number with specific format and validation using RegexValidator.
    first_name (forms.CharField): Field to capture user's first name.
    last_name (forms.CharField): Field to capture user's last name.
    email (forms.EmailField): Field to capture user's email address.
    tzname (forms.ChoiceField): Field to select a timezone from a list of common timezones.

Meta:
    model (User): The User model to be used for registration.
    fields (list): The fields to be displayed in the form for user input.
"""
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, timezone.now().year + 1)))
    phone = forms.CharField(max_length=20, 
                            help_text='\'+375 (29) XXX-XX-XX\' form, where \'X\' is digit',
                            initial='+375 (29) 000-00-00',
                            validators=[
                                RegexValidator(r'^\+375 \(29\) \d{3}\-\d{2}\-\d{2}$',
                                               'Only \'+375 (29) XXX-XX-XX\' form allowed, where \'X\' is digit')
    ])
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    tzname = forms.ChoiceField(choices=tuple((el, el) for el in COMMON_TIMEZONES))
    
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth:
            today = timezone.now().date()
            age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
            if age < 18:
                raise forms.ValidationError("Вы должны быть старше 18 лет.")
        return date_of_birth

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
class ReviewForm(forms.Form):
    """
A form for capturing user reviews with text and a numerical rating.

Attributes:
    text (forms.CharField): Field to capture the review text using a textarea widget.
    mark (forms.IntegerField): Field to capture the numerical rating with a range from 1 to 5.
"""
    text = forms.CharField(widget=forms.Textarea)
    mark = forms.IntegerField(max_value=5, min_value=1)
    
class MedicationSortSearchForm(forms.Form):
    """
A form for sorting and searching medication items.

Attributes:
    search (forms.CharField): Field to capture the search query for medication items.
    sort_by (forms.ChoiceField): Field to select the sorting criteria for medication items, with options for sorting by name or cost.
    reverse_sort (forms.BooleanField): Field to indicate whether the sorting order should be reversed.

"""
    search = forms.CharField(label='Search', required=False)
    sort_by = forms.ChoiceField(label='Sort By',
        choices=[
            ('', ''),
            ('name', 'Name'),
            ('cost', 'Cost')
            ],
        required=False)
    reverse_sort = forms.BooleanField(label='Reverse sort?', required=False)
    
class MakeOrderForm(forms.Form):
    """
A form for making an order in the pharmacy system.

Attributes:
    quantity (IntegerField): The quantity of items to order.
    department (ModelChoiceField): The pharmacy department where the order will be placed.
    promotional_code (CharField): The promotional code for applying discounts to the order.

Methods:
    clean_promotional_code(): Validates the promotional code entered by the user.

Raises:
    ValidationError: If the promotional code entered does not exist in the system.

"""
    quantity = forms.IntegerField(min_value=1)
    department = forms.ModelChoiceField(queryset=PharmacyDepartment.objects.all())
    promotional_code = forms.CharField(max_length=20, required=False)
    
    def clean_promotional_code(self):
        promo = self.cleaned_data['promotional_code']
        
        if not promo:
            return promo
        
        try:
            Promo.objects.get(promo=promo)
        except Promo.DoesNotExist:
            raise forms.ValidationError("Promotional code doesn't exist.")
        
        return promo
    
class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['name', 'instruction', 'description', 'cost', 'categories', 'supplier', 'photo']
        
class MedicationCategoryForm(forms.ModelForm):
    class Meta:
        model = MedicationCategory
        fields = ['name', 'description']

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['company_name', 'phone', 'address']

class PharmacyDepartmentForm(forms.ModelForm):
    class Meta:
        model = PharmacyDepartment
        fields = ['address']
        
class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, timezone.now().year + 1)))

    class Meta:
        model = Employee
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 
                  'date_of_birth', 'phone', 'position', 'salary', 'photo', 
                  'timezone_info', 'suppliers']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        employee_group = Group.objects.get(name='Employee')
        user.groups.add(employee_group)
        employee = super().save(commit=False)
        employee.user = user
        if commit:
            employee.save()
        return employee
    
class EmployeeUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, timezone.now().year + 1)))
    class Meta:
        model = Employee
        fields = ['username', 'email', 'first_name', 'last_name', 
                  'date_of_birth', 'phone', 'position', 'salary', 'photo', 
                  'timezone_info', 'suppliers']

    # Сохранение модели User при редактировании Employee
    def save(self, commit=True):
        employee = super().save(commit=False)
        user = employee.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            employee.save()
        return employee