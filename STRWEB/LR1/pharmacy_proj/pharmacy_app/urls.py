from django.urls import path, re_path
from . import views
from django.http import HttpResponse

app_name = 'pharmacy_app'
urlpatterns = [
    re_path(r'^$', views.default_view, name='home'),
    re_path(r'^policy/$', views.policy_view, name='policy'),
    re_path(r'^info/$', views.info_view, name='info'),
    re_path(r'^login/$', views.login_view, name='login'),
    re_path(r'^register/$', views.register_view, name='register'),
    re_path(r'^home/$', views.home_view, name='home'),
    
    re_path(r'^news/$', views.news_view, name='news'),
    re_path(r'^news/(?P<id>\d+)/$', views.news_details_view, name='news_details'),
    
    re_path(r'^shop/$', views.shop_view, name='shop'),
    re_path(r'^shop/(?P<id>\d+)/$', views.shop_order_view, name='shop_order'),
    re_path(r'^shop/delete/(?P<id>\d+)$', views.shop_medicarion_deletion, name='shop_medication_delete'),
    re_path(r'^shop/update/(?P<id>\d+)$', views.shop_medication_update_view, name='shop_medication_update'),
    re_path(r'^shop/create/$', views.shop_medication_create_view, name='shop_medication_create'),
    
    re_path(r'^categories/$', views.medication_category_list_view, name='medication_category_list'),
    re_path(r'^categories/create/$', views.medication_category_create_view, name='medication_category_create'),
    re_path(r'^categories/update/(?P<id>\d+)$', views.medication_category_update_view, name='medication_category_update'),
    re_path(r'^categories/delete/(?P<id>\d+)$', views.medication_category_delete_view, name='medication_category_delete'),
    
    re_path(r'^suppliers/$', views.supplier_list_view, name='supplier_list'),
    re_path(r'^suppliers/create/$', views.supplier_create_view, name='supplier_create'),
    re_path(r'^suppliers/update/(?P<id>\d+)$', views.supplier_update_view, name='supplier_update'),
    re_path(r'^suppliers/delete/(?P<id>\d+)$', views.supplier_delete_view, name='supplier_delete'),
    
    re_path(r'^departments/$', views.pharmacy_department_list_view, name='pharmacy_department_list'),
    re_path(r'^departments/create/$', views.pharmacy_department_create_view, name='pharmacy_department_create'),
    re_path(r'^departments/update/(?P<id>\d+)$', views.pharmacy_department_update_view, name='pharmacy_department_update'),
    re_path(r'^departments/delete/(?P<id>\d+)$', views.pharmacy_department_delete_view, name='pharmacy_department_delete'),
    
    re_path(r'^contacts/$', views.contacts_view, name='contacts'),
    re_path(r'^contacts/delete/(?P<id>\d+)$', views.employee_delete_view, name='employee_delete'),
    re_path(r'^contacts/create/$', views.employee_create_view, name='employee_create'),
    re_path(r'^contacts/update/(?P<id>\d+)$', views.employee_update_view, name='employee_update'),
    
    re_path(r'^questions/$', views.questions_view, name='questions'),
    re_path(r'^vacancies/$', views.vacancies_view, name='vacancies'),
    
    re_path(r'^reviews/$', views.reviews_view, name='reviews'),
    re_path(r'^reviews/create/$', views.review_create_view, name='review_create'),
    
    re_path(r'^promo/$', views.promo_view, name='promo'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
    re_path(r'^time/$', views.time_view, name='time'),
    re_path(r'^user/$', views.user_view, name='user'),
    re_path(r'^activity/$', views.activity_api_view, name='activity'),
    re_path(r'^cat/$', views.cat_fact_api_view, name='cat'),
]
