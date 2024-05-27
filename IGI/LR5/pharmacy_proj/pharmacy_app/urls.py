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
    re_path(r'^shop/$', views.shop_view, name='shop'),
    re_path(r'^shop/(?P<id>\d+)/$', views.shop_order_view, name='shop_order'),
    re_path(r'^questions/$', views.questions_view, name='questions'),
    re_path(r'^contacts/$', views.contacts_view, name='contacts'),
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
