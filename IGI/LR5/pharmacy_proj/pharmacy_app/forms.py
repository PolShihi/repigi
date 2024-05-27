from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from pharmacy_proj.common_timezones import COMMON_TIMEZONES
from .models import PharmacyDepartment, Promo

class LoginForm(AuthenticationForm):
    pass

class RegistrationForm(UserCreationForm):
    age = forms.IntegerField(max_value=130, min_value=18)
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

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
class ReviewForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    mark = forms.IntegerField(max_value=5, min_value=1)
    
class MedicationSortSearchForm(forms.Form):
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