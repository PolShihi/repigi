from django.shortcuts import render, redirect, get_object_or_404
from django.template import Template, Context
from django.http import HttpRequest, HttpResponseNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from .models import *
from .forms import *
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
    """
Render the 'policy.html' template to display the policy view.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The HTTP response object rendering the 'policy.html' template.
"""
    logger.info(policy_view.__name__ + ' is called')
    return render(request, "policy.html")


def info_view(request: HttpRequest):
    """
Renders the 'info.html' template with the company information retrieved from the database.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered template with the company information.

Logs:
    - Logs an info message when the function is called.
    - Logs a warning message if there is no company information in the database.
    - Logs an info message if there is company information in the database.
"""
    logger.info(info_view.__name__ + ' is called')
    company_info = CompanyInfo.objects.last()

    info = "No info"
    if company_info:
        logger.info('There is company info in database')
        info = company_info.text
    else:
        logger.warning('No company info in database')

    return render(request, "info.html", {"info": info})


def login_view(request: HttpRequest):
    """
View function for user login.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The HTTP response object.

Behavior:
    - If the user is already authenticated, redirects to the home page.
    - If the request method is POST, validates the login form data.
    - If the form is valid, authenticates the user and logs them in.
    - If the form is invalid, renders the login form again.
    - If the request method is not POST, renders the login form.

Logs:
    - Logs the function call.
    - Logs warnings for user already authenticated and invalid form data.
    - Logs errors for authentication failure.

Template:
    - Renders the 'login.html' template with the login form.

"""
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
    """
Register a new user by processing the registration form data.

Parameters:
    request (HttpRequest): The HTTP request object containing the form data.

Returns:
    HttpResponse: A redirect response to the login page if the registration is successful, 
    or a rendered registration form page with error messages if the form data is invalid.

Logs:
    - Logs an info message when the function is called.
    - Logs a warning if the form data is invalid or if the username is already in use.

Form Validation:
    - Validates the registration form data including username, email, password, first name, last name, age, phone, and timezone selection.
    - Checks if the username is unique before creating a new user.
    - Assigns the new user to the 'Client' group and creates a Client instance with additional user information.

Redirects:
    - Redirects to the login page upon successful registration.

Template:
    - Renders the 'register.html' template with the registration form for user input.

"""
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
                                date_of_birth=form.cleaned_data['date_of_birth'],
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
    """
Logs out the current user and deactivates the timezone before redirecting to the login page.

Parameters:
    request (HttpRequest): The HTTP request object containing metadata about the request.

Returns:
    HttpResponseRedirect: Redirects to the login page after logging out the user and deactivating the timezone.
"""
    logger.info(logout_view.__name__ + ' is called')
    logout(request)
    timezone.deactivate()
    return redirect('pharmacy:login')


def reviews_view(request: HttpRequest):
    """
View function to display all reviews.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: Rendered template with all reviews.

"""
    logger.info(reviews_view.__name__ + ' is called')
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})


@login_required
def review_create_view(request: HttpRequest):
    """
View function for creating a new review.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: Redirects to the 'reviews' page if the form is valid, otherwise renders the 'review_create.html' template with the form.

Requires:
    The user to be logged in.

Form:
    ReviewForm: A form for capturing user reviews with text and a numerical rating.
        - text (forms.CharField): Field to capture the review text using a textarea widget.
        - mark (forms.IntegerField): Field to capture the numerical rating with a range from 1 to 5.
"""
    logger.info(review_create_view.__name__ + ' is called')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            logger.info('Form is valid')
            user = User.objects.get(id=request.user.id)
            full_name = user.first_name + ' ' + user.last_name
            review = Review(
                full_name=full_name, mark=form.cleaned_data['mark'], text=form.cleaned_data['text'])
            review.save()
            return redirect('pharmacy:reviews')
        else:
            logger.warning('Form has invalid data')
    else:
        form = ReviewForm()

    return render(request, 'review_create.html', {'form': form})


def promo_view(request: HttpRequest):
    """
Renders the 'promo.html' template with active and archived Promo objects.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered template with active and archived Promo objects.

"""
    logger.info(promo_view.__name__ + ' is called')
    promo_active = Promo.objects.filter(is_active=True)
    promo_archived = Promo.objects.filter(is_active=False)
    return render(request, 'promo.html', {'promo_active': promo_active, 'promo_archived': promo_archived})


def questions_view(request: HttpRequest):
    """
View function to render the 'questions.html' template with all QuestionAnswer objects.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: Rendered template with all QuestionAnswer objects passed as context.

"""
    logger.info(questions_view.__name__ + ' is called')
    questions = QuestionAnswer.objects.all()
    return render(request, 'questions.html', {'questions': questions})


def time_view(request: HttpRequest):
    """
View function for handling timezone selection and displaying current time and calendar.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered HTML response with timezone selection options, current time, and calendar.
"""
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

    return render(request, "time.html", {"timezones": tuple((el, el) for el in COMMON_TIMEZONES), 'now': date_now, 'calendar': callen.formatmonth(date_now.year, date_now.month)})


def vacancies_view(request: HttpRequest):
    """
Renders the 'vacancies.html' template with a context containing all instances of Vacancy model.

Parameters:
    request (HttpRequest): The HTTP request object sent by the user.

Returns:
    HttpResponse: The HTTP response object that renders the 'vacancies.html' template with the vacancies context.

"""
    logger.info(vacancies_view.__name__ + ' is called')
    vacancies = Vacancy.objects.all()
    return render(request, 'vacancies.html', {'vacancies': vacancies})


def contacts_view(request: HttpRequest):
    """
Renders the 'contacts.html' template with a list of all employees.

Parameters:
- request (HttpRequest): The HTTP request object.

Returns:
- HttpResponse: The HTTP response object that renders the 'contacts.html' template with a context containing all employees.

"""
    logger.info(contacts_view.__name__ + ' is called')
    employees = Employee.objects.all()
    return render(request, 'contacts.html', {'employees': employees})


@login_required
def shop_view(request: HttpRequest):
    """
View function for displaying the shop page with medication items.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered HTML page displaying medication items based on search and sorting criteria.

"""
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
    """
View function for placing an order in the pharmacy system.

Parameters:
    request (HttpRequest): The HTTP request object.
    id (int): The id of the medication to be ordered.

Returns:
    HttpResponse: Renders the 'shop_make_order.html' template with the order form and medication details.

Restrictions:
    - Only users in the 'Client' group can access this view.

Behavior:
    - Retrieves the medication object based on the provided id.
    - Handles form submission for making an order.
    - Validates the form data and creates an order if the form is valid.
    - Logs relevant information using the logger.
    - Renders the order form template with necessary context data.

Raises:
    - Http404: If the medication with the provided id does not exist.

"""
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
            promo = Promo.objects.get(
                promo=form.cleaned_data['promotional_code']) if form.cleaned_data['promotional_code'] else None
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
    """
View function for displaying user information based on their group membership.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: Rendered HTML template displaying user information based on their group membership, or redirects to admin page if user does not belong to any group.
"""
    logger.info(user_view.__name__ + ' is called')

    if is_in_groups('Client')(request.user):
        logger.info('User is client')
        client = Client.objects.get(user_id=request.user.id)
        return render(request, 'user_client.html', {'client': client})

    if is_in_groups('Employee')(request.user):
        logger.info('User is employee')
        employee = Employee.objects.get(user_id=request.user.id)
        orders = [order for supplier in employee.suppliers.all()
                  for order in supplier.get_list_of_orders() if order.is_paid]
        total_revenue = sum([order.get_total_cost() for order in orders])
        return render(request, 'user_employee.html', {'employee': employee, 'orders': orders, 'total_revenue': total_revenue})

    return redirect('/admin')


def home_view(request: HttpRequest):
    """
Renders the home page view based on the user's authentication status and group membership.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The rendered home page view with context data.
"""
    logger.info(home_view.__name__ + ' is called')

    if not request.user.is_authenticated or is_in_groups('Client')(request.user):
        logger.info('User is client or not authenticated')
        news = None
        company_info = None
        add_banners = None
        try:
            news = News.objects.latest('posted_date')
        except News.DoesNotExist:
            logger.warning('There is no news')
            
        try:
            company_info = CompanyInfo.objects.first()
        except CompanyInfo.DoesNotExist:
            logger.warning('There is no company info')
            
        try:
            add_banners = AddBanner.objects.all()
        except AddBanner.DoesNotExist:
            logger.warning('There is no add baners')
            
        try:
            partners = Partner.objects.all()
        except AddBanner.DoesNotExist:
            logger.warning('There is no add baners')
            
        return render(request, 'home.html', {'news': news, 'company_info': company_info, 'add_banners': add_banners, 'partners': partners})

    context = {}
    medications = list(Medication.objects.all())
    context['sorted_medications'] = Medication.objects.order_by("name")

    revenue_list = [medication.get_total_revenue()
                    for medication in medications]
    if revenue_list:
        context['average_revenue'] = statistics.mean(revenue_list)
        context['mode_revenue'] = statistics.mode(revenue_list)
        context['median_revenue'] = statistics.median(revenue_list)

    clients_age_list = [client.get_age() for client in Client.objects.all()]
    if clients_age_list:
        context['average_age'] = statistics.mean(clients_age_list)
        context['median_age'] = statistics.median(clients_age_list)

    if medications:
        context['most_popular_medication'] = max(
            medications, key=lambda m: m.get_total_number_of_ordered())
        context['most_profitable_medication'] = max(
            medications, key=lambda m: m.get_total_revenue())

        fig, ax = plt.subplots(figsize=(15, 6))
        ax.bar([medication.name for medication in medications], [
               medication.get_total_revenue() for medication in medications])
        ax.set_xlabel('Medication')
        ax.set_ylabel('Revenue, $')
        ax.set_xticks([medication.name for medication in medications])
        ax.set_xticklabels(
            [medication.name for medication in medications], fontsize=6)
        ax.set_title('Total Revenue by Medication')
        fig.savefig(os.path.join(MEDIA_ROOT, 'chart.png'), bbox_inches='tight')
        context['chart_url'] = MEDIA_URL + 'chart.png'

    return render(request, 'home_details.html', context)


def default_view(request: HttpRequest):
    """
View function for redirecting to the home page.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponseRedirect: Redirects to the 'home' URL.
"""
    logger.info(default_view.__name__ + ' is called')
    return redirect('pharmacy:home')


@login_required
def cat_fact_api_view(request: HttpRequest):
    """
Render the 'policy.html' template to display the policy view.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: The HTTP response object rendering the 'policy.html' template.
"""
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
    """
Render a random activity fetched from an external API.

Parameters:
    request (HttpRequest): The HTTP request object.

Returns:
    HttpResponse: A rendered HTML template displaying the fetched activity or an error message if the activity fetching or parsing fails.
"""
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
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Error parsing activity response: {e}")
        return render(request, 'api_activity.html', {'error': 'Failed to parse activity response'})

    return render(request, 'api_activity.html', {'activity': activity})


@login_required
@user_passes_test(is_in_groups('Admin'))
def shop_medicarion_deletion(request: HttpRequest, id):
    med = Medication.objects.get(id=id)
    med.delete()
    return redirect('pharmacy:shop')


@login_required
@user_passes_test(is_in_groups('Admin'))
def shop_medication_update_view(request: HttpRequest, id):
    try:
        medication = Medication.objects.get(id=id)
    except Medication.DoesNotExist:
        logger.warning(f'There is no medication with id={id}')
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES, instance=medication)

        if form.is_valid():
            form.save()
            return redirect('pharmacy:shop')
        else:
            logger.warning('Form has invalid data')
            form.add_error(None, 'Input data is invalid.')
    else:
        form = MedicationForm(instance=medication)

    return render(request, 'shop_update_create.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def shop_medication_create_view(request: HttpRequest):
    if request.method == 'POST':
        form = MedicationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('pharmacy:shop')
        else:
            logger.warning('Form has invalid data')
            form.add_error(None, 'Input data is invalid.')
    else:
        form = MedicationForm()

    return render(request, 'shop_update_create.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def medication_category_list_view(request):
    categories = MedicationCategory.objects.all()
    return render(request, 'medication_category/list.html', {'categories': categories})


@login_required
@user_passes_test(is_in_groups('Admin'))
def medication_category_create_view(request):
    if request.method == 'POST':
        form = MedicationCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:medication_category_list')
    else:
        form = MedicationCategoryForm()
    return render(request, 'medication_category/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def medication_category_update_view(request, id):
    category = get_object_or_404(MedicationCategory, pk=id)
    if request.method == 'POST':
        form = MedicationCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:medication_category_list')
    else:
        form = MedicationCategoryForm(instance=category)
    return render(request, 'medication_category/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def medication_category_delete_view(request, id):
    category = get_object_or_404(MedicationCategory, pk=id)
    category.delete()
    return redirect('pharmacy:medication_category_list')


@login_required
@user_passes_test(is_in_groups('Admin'))
def supplier_list_view(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier/list.html', {'suppliers': suppliers})


@login_required
@user_passes_test(is_in_groups('Admin'))
def supplier_create_view(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'supplier/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def supplier_update_view(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'supplier/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def supplier_delete_view(request, id):
    supplier = get_object_or_404(Supplier, pk=id)
    supplier.delete()
    return redirect('pharmacy:supplier_list')


@login_required
@user_passes_test(is_in_groups('Admin'))
def pharmacy_department_list_view(request):
    pharmacy_departments = PharmacyDepartment.objects.all()
    return render(request, 'pharmacy_department/list.html', {'departments': pharmacy_departments})


@login_required
@user_passes_test(is_in_groups('Admin'))
def pharmacy_department_create_view(request):
    if request.method == 'POST':
        form = PharmacyDepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:pharmacy_department_list')
    else:
        form = PharmacyDepartmentForm()
    return render(request, 'pharmacy_department/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def pharmacy_department_update_view(request, id):
    pharmacy_department = get_object_or_404(PharmacyDepartment, pk=id)
    if request.method == 'POST':
        form = PharmacyDepartmentForm(
            request.POST, instance=pharmacy_department)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:pharmacy_department_list')
    else:
        form = PharmacyDepartmentForm(instance=pharmacy_department)
    return render(request, 'pharmacy_department/form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def pharmacy_department_delete_view(request, id):
    pharmacy_department = get_object_or_404(PharmacyDepartment, pk=id)
    pharmacy_department.delete()
    return redirect('pharmacy:pharmacy_department_list')


@login_required
@user_passes_test(is_in_groups('Admin'))
def employee_create_view(request):
    if request.method == 'POST':
        form = EmployeeCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:contacts')
    else:
        form = EmployeeCreateForm()
    return render(request, 'employee_form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def employee_update_view(request, id):
    employee = get_object_or_404(Employee, pk=id)

    if request.method == 'POST':
        form = EmployeeUpdateForm(
            request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('pharmacy:contacts')
    else:
        form = EmployeeUpdateForm(initial={
                'username': employee.user.username,
                'email': employee.user.email,
                'first_name': employee.user.first_name,
                'last_name': employee.user.last_name,
            },instance=employee)

    return render(request, 'employee_form.html', {'form': form})


@login_required
@user_passes_test(is_in_groups('Admin'))
def employee_delete_view(request, id):
    employee = get_object_or_404(Employee, pk=id)
    user = employee.user
    user.delete()
    employee.delete()
    return redirect('pharmacy:contacts')


def news_view(request):
    logger.info(news_view.__name__ + ' is called')
    news_list = News.objects.all()
    return render(request, 'news.html', {'news_list': news_list})


def news_details_view(request, id):
    news = get_object_or_404(News, id=id)
    return render(request, 'news_details.html', {'news': news})

@login_required
def order_pay_view(request, id):
    order = get_object_or_404(Order, pk=id)
    order.is_paid = True
    order.save()
    return redirect('pharmacy:user')

def about_view(request):
    company_info = CompanyInfo.objects.first()
    company_history = CompanyHistory.objects.all()
    partners = Partner.objects.all()
    certificate = Template(company_info.certificate).render(Context({'company_info': company_info}))
    
    return render(request, 'about.html', {'company_info': company_info, 'certificate': certificate, 'company_history': company_history, 'partners': partners})

def html_stuff_view(request):
    return render(request, 'html_stuff.html')