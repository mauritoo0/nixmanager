"""
URL configuration for nixreservas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from vips import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('main/', views.main, name='main'),

    # Authentication
    path('sign_up/', views.sign_up, name='sign_up'),
    path('log_in/', views.log_in, name='log_in'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # Promoters
    path('promoters/', views.promoters, name='promoters'),
    path('promoters/new/', views.new_promoter, name='new_promoter'),
    path('promoters/<int:promoter_id>/', views.edit_promoter, name='edit_promoter'),
    path('promoters/<int:promoter_id>/delete/', views.delete_promoter, name='delete_promoter'),

    # Customers
    path('customers/', views.customers, name='customers'),
    path('customers/new/', views.new_customer, name='new_customer'),
    path('customers/<int:customer_id>/', views.edit_customer, name='edit_customer'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),

    # Tables
    path('tables/', views.tables, name='tables'),
    path('tables/new/', views.new_table, name='new_table'),
    path('tables/<int:table_id>/', views.edit_table, name='edit_table'),
    path('tables/<int:table_id>/delete/', views.delete_table, name='delete_table'),

    # Reservations
    path('reservations/', views.reservations, name='reservations'),
    path('reservations/new/', views.new_reservation, name='new_reservation'),
    path('reservations/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('reservations/<int:reservation_id>/delete/', views.delete_reservation, name='delete_reservation'),
]
