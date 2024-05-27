from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import *
from .forms import LoginForm, RegistrationForm, ReviewForm, MedicationSortSearchForm, MakeOrderForm
from django.contrib.auth.decorators import login_required, user_passes_test
from pharmacy_proj.common_timezones import COMMON_TIMEZONES
from django.utils import timezone
from .usefuls import is_in_groups
import zoneinfo
import calendar
import statistics
import matplotlib.pyplot as plt
import os
import requests
import logging
from pharmacy_proj.settings import MEDIA_ROOT, MEDIA_URL

logger = logging.getLogger(__name__)

# Create your views here.
def policy_view(request: HttpRequest):
    logger.info(policy_view.__name__ + ' is called')
    return render(request, "policy.html")

def info_view(request: HttpRequest):
    logger.info(info_view.__name__ + ' is called')
    company_info = CompanyInfo.objects.last()
    
    info = "No info"
    if company_info:
        logger.info('There is company info in database')
        info = company_info.text
    else:
        logger.warning('No company info in database')
        
    return render(request, "info.html", {"info" : info})

def login_view(request: HttpRequest):
    logger.info(login_view.__name__ + ' is called')
    
    if request.user.is_authenticated:
        logger.warning('User is already authenticated')
        return redirect('pharmacy:home')
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            logger.info('Form is valid')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('pharmacy:home')
            
            logger.error('User is None')
        else:
            logger.warning('Form has invalid data')
    else:
        form = LoginForm()
        
    return render(request, 'login.html', {'form': form})

def register_view(request: HttpRequest):
    logger.info(register_view.__name__ + ' is called')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')
            try:
                user = User.objects.get(username=form.cleaned_data['username'])
            except User.DoesNotExist:
                logger.warning('The user who registers has a unique username')
                user = User.objects.create_user(username=form.cleaned_data['username'],
                                                email=form.cleaned_data['email'],
                                                password=form.cleaned_data['password1'],
                                                first_name=form.cleaned_data['first_name'],
                                                last_name=form.cleaned_data['last_name'],)
                client_group = Group.objects.get(name='Client')
                user.groups.add(client_group)
                client = Client(user_id=user.pk,
                                age=form.cleaned_data['age'],
                                phone=form.cleaned_data['phone'],
                                timezone_info=form.cleaned_data['tzname'])
                client.save()
                return redirect('pharmacy:login')
                
            logger.warning('Username is already used')
            form.add_error(None, 'Username is already used.')
        else:
            logger.warning('Form has invalid data')
            form.add_error(None, 'Input data is invalid.')
    else:
        form = RegistrationForm()
        
    return render(request, 'register.html', {'form': form})

def logout_view(request: HttpRequest):
    logger.info(logout_view.__name__ + ' is called')
    logout(request)
    timezone.deactivate()
    return redirect('pharmacy:login')

def reviews_view(request: HttpRequest):
    logger.info(reviews_view.__name__ + ' is called')
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

@login_required
def review_create_view(request: HttpRequest):
    logger.info(review_create_view.__name__ + ' is called')
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')
            user = User.objects.get(id=request.user.id)
            full_name = user.first_name + ' ' + user.last_name
            review = Review(full_name=full_name, mark=form.cleaned_data['mark'], text=form.cleaned_data['text'])
            review.save()
            return redirect('pharmacy:reviews')
        else:
            logger.warning('Form has invalid data')
    else:
        form = ReviewForm()
        
    return render(request, 'review_create.html', {'form': form})

def promo_view(request: HttpRequest):
    logger.info(promo_view.__name__ + ' is called')
    promo_active = Promo.objects.filter(is_active=True)
    promo_archived = Promo.objects.filter(is_active=False)
    return render(request, 'promo.html', {'promo_active': promo_active, 'promo_archived': promo_archived})

def questions_view(request: HttpRequest):
    logger.info(questions_view.__name__ + ' is called')
    questions = QuestionAnswer.objects.all()
    return render(request, 'questions.html', {'questions': questions})

def time_view(request: HttpRequest):
    logger.info(time_view.__name__ + ' is called')
    
    if request.method == "POST":
        if request.user.is_authenticated:
            logger.info('User is authenticated')

            if is_in_groups('Client')(request.user):
                logger.info('User is client')
                client = Client.objects.get(user_id=request.user.id)
                client.timezone_info = request.POST["timezone"]
                client.save()
                
            if is_in_groups('Employee')(request.user):
                logger.info('User is employee')
                employee = Employee.objects.get(user_id=request.user.id)
                employee.timezone_info = request.POST["timezone"]
                employee.save()
                
        request.session["django_timezone"] = request.POST["timezone"]
        timezone.activate(zoneinfo.ZoneInfo(request.POST["timezone"]))
        
    date_now = timezone.now()
    callen = calendar.HTMLCalendar()
        
    return render(request, "time.html", {"timezones": tuple((el, el) for el in COMMON_TIMEZONES), 'now': date_now, 'calendar' : callen.formatmonth(date_now.year, date_now.month)})

def vacancies_view(request: HttpRequest):
    logger.info(vacancies_view.__name__ + ' is called')
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})

def contacts_view(request: HttpRequest):
    logger.info(contacts_view.__name__ + ' is called')
    employees = Employee.objects.all()
    return render(request, 'contacts.html', {'employees': employees})

@login_required
def shop_view(request: HttpRequest):
    logger.info(shop_view.__name__ + ' is called')
    form = MedicationSortSearchForm(request.GET)
    medications = Medication.objects.all()

    if form.is_valid():
        logger.info('Form is valid')
        search = form.cleaned_data.get('search')
        sort_by = form.cleaned_data.get('sort_by')

        if search:
            logger.info('Request has search parameter')
            medications = medications.filter(name__icontains=search)

        if sort_by:
            logger.info('Request has sort_by parameter')
            if form.cleaned_data.get('reverse_sort'):
                sort_by = '-' + sort_by
            medications = medications.order_by(sort_by)
    else:
        logger.warning('Form has invalid data')
    
    if is_in_groups('Client')(request.user):
        return render(request, 'shop_client.html', {'form': form, 'medications': medications})
    
    return render(request, 'shop_employee.html', {'form': form, 'medications': medications})

@user_passes_test(is_in_groups('Client'))
def shop_order_view(request: HttpRequest, id):
    logger.info(shop_order_view.__name__ + ' is called')
    try:
        medication = Medication.objects.get(id=id)
    except Medication.DoesNotExist:
        logger.warning(f'There is no medication with id={id}')
        return HttpResponseNotFound()
    
    if request.method == 'POST':
        form = MakeOrderForm(request.POST)
        
        if form.is_valid():
            logger.info('Form is valid')
            client = Client.objects.get(user_id=request.user.id)
            promo = Promo.objects.get(promo=form.cleaned_data['promotional_code']) if form.cleaned_data['promotional_code'] else None
            order = Order(
                medication_id=int(id),
                client_id=client.id,
                department=form.cleaned_data['department'],
                quantity=form.cleaned_data['quantity'],
                promo=promo
            )
            order.save()
            return redirect('pharmacy:user')
        else:
            logger.warning('Form has invalid data')
            form.add_error(None, 'Input data is invalid.')
    else:
        form = MakeOrderForm()
    
    return render(request, 'shop_make_order.html', {'form': form, 'medication': medication})

@login_required
def user_view(request: HttpRequest):
    logger.info(user_view.__name__ + ' is called')
    
    if is_in_groups('Client')(request.user):
        logger.info('User is client')
        client = Client.objects.get(user_id=request.user.id)
        return render(request, 'user_client.html', {'client': client})
    
    if is_in_groups('Employee')(request.user):
        logger.info('User is employee')
        employee = Employee.objects.get(user_id=request.user.id)
        orders = [order for supplier in employee.suppliers.all() for order in supplier.get_list_of_orders()]
        total_revenue = sum([order.get_total_cost() for order in orders])
        return render(request, 'user_employee.html', {'employee': employee, 'orders': orders, 'total_revenue': total_revenue})
    
    return redirect('/admin')

def home_view(request: HttpRequest):
    logger.info(home_view.__name__ + ' is called')
    
    if not request.user.is_authenticated or is_in_groups('Client')(request.user):
        logger.info('User is client or not authenticated')
        medication = None
        try:
            medication = Medication.objects.latest('cost')
        except Medication.DoesNotExist:
            logger.warning('There is no medications')
            medication = None
        return render(request, 'home.html', {'medication': medication,})
    
    context = {}
    medications = list(Medication.objects.all())
    context['sorted_medications'] = Medication.objects.order_by("name")
    
    revenue_list = [medication.get_total_revenue() for medication in medications]
    if revenue_list:
        context['average_revenue'] = statistics.mean(revenue_list)
        context['mode_revenue'] = statistics.mode(revenue_list)
        context['median_revenue'] = statistics.median(revenue_list)
    
    clients_age_list = [client.age for client in Client.objects.all()]
    if clients_age_list:
        context['average_age'] = statistics.mean(clients_age_list)
        context['median_age'] = statistics.median(clients_age_list)

    if medications:
        context['most_popular_medication'] = max(medications, key=lambda m: m.get_total_number_of_ordered())
        context['most_profitable_medication'] = max(medications, key=lambda m: m.get_total_revenue())
    
        fig, ax = plt.subplots()
        ax.bar([medication.name for medication in medications], [medication.get_total_revenue() for medication in medications])
        ax.set_xlabel('Medication')
        ax.set_ylabel('Revenue, $')
        ax.set_title('Total Revenue by Medication')
        fig.savefig(os.path.join(MEDIA_ROOT, 'chart.png'))
        context['chart_url'] = MEDIA_URL + 'chart.png'
    
    return render(request, 'home_details.html', context)
    
    
def default_view(request: HttpRequest):
    logger.info(default_view.__name__ + ' is called')
    return redirect('pharmacy:home')

@login_required
def cat_fact_api_view(request: HttpRequest):
    logger.info(cat_fact_api_view.__name__ + ' is called')
    api_url = 'https://catfact.ninja/fact'
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching cat fact: {e}")
        return render(request, 'api_cat.html', {'error': 'Failed to fetch cat fact'})

    try:
        fact = response.json()['fact']
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Error parsing cat fact response: {e}")
        return render(request, 'api_cat.html', {'error': 'Failed to parse cat fact response'})
    
    return render(request, 'api_cat.html', {'fact': fact})

@login_required
def activity_api_view(request: HttpRequest):
    logger.info(activity_api_view.__name__ + ' is called')
    api_url = 'https://www.boredapi.com/api/activity'
    
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching activity: {e}")
        return render(request, 'api_activity.html', {'error': 'Failed to fetch activity'})

    try:
        activity = response.json()['activity']
    except  requests.exceptions.JSONDecodeError as e:
        logger.error(f"Error parsing activity response: {e}")
        return render(request, 'api_activity.html', {'error': 'Failed to parse activity response'})
    
    return render(request, 'api_activity.html', {'activity': activity})

def news_view(request: HttpRequest):
    logger.info(news_view.__name__ + ' is called')
    medication = None
    
    try:
        medication = Medication.objects.latest('date_created')
    except:
        logger.warning('There is no medications')
        medication = None
        
    return render(request, 'news.html', {'medication': medication})
    
    
    
    