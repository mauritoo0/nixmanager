from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.db import IntegrityError
from vips.models import Promoter, Customer, Table, Reservation
from django.db.models import Q

# ----------------- INDEX -----------------
def index(request):
    return render(request, "log/index.html", {
        'title': 'Nix',
    })

# ----------------- SIGN UP -----------------
def sign_up(request):
    if request.method == 'GET':
        return render(request, "log/sign_up.html", {
            'title': 'Sign up',
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:#Create a new user and then a new promoter automatically
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                Promoter.objects.create(user=user, first_name=user.username)
                login(request, user)
                return redirect('main')
            except IntegrityError:#Exceptions if user already exist or passwords doesnt match
                return render(request, "log/sign_up.html", {
                    'title': 'Sign up',
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request, "log/sign_up.html", {
            'title': 'Sign up',
            'form': UserCreationForm,
            'error': 'Passwords do not match or do not meet the requirements'
        })


# ----------------- LOG IN -----------------
def log_in(request):
    if request.method == 'GET':
        return render(request, "log/log_in.html", {
            'title': 'Log in',
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is None:#Exception if username or password doesnt match
            return render(request, "log/log_in.html", {
                'title': 'Log in',
                'form': AuthenticationForm,
                'error': 'Incorrect username or password'
            })
        else:
            login(request, user)
            return redirect('main')
        
        
# ----------------- LOGOUT -----------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('index')



# ----------------- PROFILE -----------------
@login_required
def profile(request):
    return render(request, "log/profile.html")


# ----------------- EDIT PROFILE -----------------
@login_required
def edit_profile(request):
    title = "Edit profile"
    if request.method == 'POST':#Editing profile
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            password1 = form.cleaned_data.get("password1")#Editing password if user wants to
            if password1:
                request.user.set_password(password1)
                request.user.save()
                update_session_auth_hash(request, request.user)

            return redirect('profile')
        else:#Exception if fields doesnt match
            return render(request, 'log/edit_profile.html',
                          {'form': form,
                           'title': title,
                           'error': 'Please check the fields carefully. '
                                    'The username may already exist or the email may be invalid.'
                           })

    else:
        return render(request, 'log/edit_profile.html',
                      {'form': EditProfileForm(instance=request.user),
                       'title': title,
                       })

# ----------------- MAIN.HTML -----------------
@login_required
def main(request):#Show a table with customers and reservations from the request user
    total_customers = Customer.objects.filter(user=request.user).count()
    total_reservations = Reservation.objects.filter(user=request.user).count()
    
    
    return render(request, 'main.html', {
        'total_customers': total_customers,
        'total_reservations': total_reservations,
        
    })


# ----------------- PROMOTERS -----------------
@login_required
def promoters(request):
    form = SearchPromoterForm(request.GET or None)#search bar to search promoters
    order_by = request.GET.get('sort', '-id')#Promoters sorted
    promoters = Promoter.objects.all().order_by(order_by)#Table to show all promotors 

    if form.is_valid():
        filtered_promoter = form.cleaned_data.get('b_promoter')#Filter from the search bar to search promoters
        if filtered_promoter:#User can search by all this filters: 
            promoters = promoters.filter(
                Q(first_name__icontains=filtered_promoter) |
                Q(last_name__icontains=filtered_promoter) |
                Q(area__icontains=filtered_promoter)
            )

    return render(request, 'promoters/promoters.html', {
        'promoters': promoters,
        'title': 'Promoters',
        'form': form
    })


# ----------------- NEW PROMOTER -----------------
@login_required
def new_promoter(request):
    if request.method == 'GET':
        return render(request, 'promoters/new_promoter.html', {
            'form': PromoterForm,
            'title': 'New promoter'
        })
    else:
        try:#Form to create a new promoter
            form = PromoterForm(request.POST)
            new_promoter = form.save(commit=False)
            new_promoter.user = request.user
            new_promoter.save()
            return redirect('promoters')

        except ValueError:#Exception if there is an error on fields
            return render(request, 'promoters/new_promoter.html', {
                'form': form,
                'error': 'Please check the fields carefully'
            })

# ----------------- EDIT PROMOTER -----------------
@login_required
def edit_promoter(request, promoter_id):
    promoter = get_object_or_404(Promoter, pk=promoter_id)
    if request.method == 'GET': #Form to edit promoter
        form = PromoterForm(instance=promoter)
        return render(request, 'promoters/edit_promoter.html', {
            'title': 'Edit promoter',
            'promoter': promoter,
            'form': form
        })
    else:
        try:#Saving promoter if everything is ok
            form = PromoterForm(request.POST, instance=promoter)
            form.save()
            return redirect('promoters')
        except ValueError:#Exception if there is an error on fields
            return render(request, 'promoters/edit_promoter.html', {
                'title': 'Edit promoter',
                'promoter': promoter,
                'form': form,
                'error': 'Please check the fields carefully'
            })


# ----------------- DELETE PROMOTER -----------------
@login_required
def delete_promoter(request, promoter_id):
    promoter = get_object_or_404(Promoter, pk=promoter_id)
    if request.method == 'POST':#Deleting promoter and redirect to "promoters"
        promoter.delete()
        return redirect('promoters')

    return render(request, 'promoters/promoters.html')



# ----------------- CUSTOMERS -----------------
@login_required
def customers(request):
    order_by = request.GET.get('sort', '-id')#search bar to search customers
    customers = Customer.objects.all().order_by(order_by)#Customers sorted
    form = SearchCustomerForm(request.GET or None)#Table to show all customers

    if form.is_valid():
        filtered_customer = form.cleaned_data.get('b_customer')#Filter from the search bar to search customers
        if filtered_customer:#User can search by all this filters: 
            customers = customers.filter(
                Q(first_name__icontains=filtered_customer) |
                Q(last_name__icontains=filtered_customer) |
                Q(city__icontains=filtered_customer) |
                Q(nationality__icontains=filtered_customer) |
                Q(email__icontains=filtered_customer) |
                Q(promoter__first_name__icontains=filtered_customer)
            )

    return render(request, "customers/customers.html", {
        'title': 'Customers',
        'customers': customers,
        'form': form
    })


# ----------------- NEW CUSTOMER -----------------
@login_required
def new_customer(request):
    if request.method == 'GET':
        return render(request, 'customers/new_customer.html', {
            'title': 'New customer',
            'form': CustomerForm
        })
    else:#Saving customer if everything is ok
        form = CustomerForm(request.POST)
        if form.is_valid():
            new_customer = form.save(commit=False)
            new_customer.user = request.user
            new_customer.save()
            return redirect('customers')

        else:#Exception if there is an error on fields
            return render(request, 'customers/new_customer.html', {
                'title': 'New customer',
                'form': form,
                'error': 'Please check the fields carefully (valid email, etc)'
            })


# ----------------- EDIT CUSTOMER -----------------
@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'GET':
        form = CustomerForm(instance=customer)
        return render(request, "customers/edit_customer.html", {
            'title': 'Edit customer',
            'customer': customer,
            'form': form,
        })
    else:
        try:#Saving customer if everything is ok
            form = CustomerForm(request.POST, instance=customer)
            form.save()
            return redirect('customers')
        except ValueError:#Exception if there is an error on fields
            return render(request, "customers/edit_customer.html", {
                'title': 'Edit customer',
                'customer': customer,
                'form': form,
                'error': 'Please check the fields carefully (valid email, etc)'
            })


@login_required
def delete_customer(request, customer_id):
    customer = get_object_or_404(Customer, pk=customer_id)
    if request.method == 'POST':
        customer.delete()
        return redirect('customers')

    return render(request, 'customers/customers.html')


# ----------------- TABLES -----------------
@login_required
def tables(request):
    order_by = request.GET.get('sort', 'id')#Tables sorted
    tables = Table.objects.all().order_by(order_by)#Table to show all tables
    return render(request, "tables/tables.html", {
        'title': 'Tables',
        'tables': tables
    })


# ----------------- NEW TABLE -----------------
@login_required
def new_table(request):
    form = TableForm()
    if request.method == 'GET':
        return render(request, 'tables/new_table.html', {
            'title': 'New table',
            'form': form
        })
    else:#Saving table if everything is ok
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tables')
        else:#Exception if there is an error on fields
            return render(request, 'tables/new_table.html', {
                'title': 'New table',
                'form': form,
                'error': 'Please check the fields carefully'
            })


@login_required
def edit_table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    if request.method == 'GET':
        form = TableForm(instance=table)
        return render(request, 'tables/edit_table.html', {
            'title': 'Edit table',
            'table': table,
            'form': form
        })
    else:#Saving table if everything is ok
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            table.save()
            return redirect('tables')


# ----------------- DELETE TABLE -----------------
@login_required
def delete_table(request, table_id):
    table = get_object_or_404(Table, pk=table_id)
    if request.method == 'POST':
        table.delete()
        return redirect('tables')

    return render(request, 'customers/customers.html')


# ----------------- RESERVATIONS -----------------
@login_required
def reservations(request):
    order_by = request.GET.get('sort', '-id')#Reservations sorted
    reservations = Reservation.objects.all().order_by(order_by)#Table to show all reservations
    form = SearchReservationForm(request.GET or None)#Form to search reservation by a hint 
    date_form = ReservationDateForm(request.GET or None)#search bar to search reservation by date

    if form.is_valid():
        filtered_reservation = form.cleaned_data.get('b_reservation')#Filter from the search bar to search reservation
        if filtered_reservation:#User can search by all this filters: 
            reservations = reservations.filter( 
                Q(customer__first_name__icontains=filtered_reservation) |
                Q(table__number__icontains=filtered_reservation) |
                Q(date__icontains=filtered_reservation) |
                Q(promoter__first_name__icontains=filtered_reservation)
            )

    if date_form.is_valid():#User can search by date with another search bar too: 
        start_date = date_form.cleaned_data.get('start_date')
        end_date = date_form.cleaned_data.get('end_date')

        if start_date and end_date:#Filters to search by start and end date
            reservations = reservations.filter(date__range=(start_date, end_date))
        elif start_date:
            reservations = reservations.filter(date__gte=start_date)
        elif end_date:
            reservations = reservations.filter(date__lte=end_date)

    return render(request, "reservations/reservations.html", {
        'title': 'Reservations',
        'reservations': reservations,
        'form': form,
        'date_form': date_form
    })


# ----------------- NEW RESERVATION -----------------
@login_required
def new_reservation(request):
    form = ReservationForm()
    if request.method == 'GET':
        return render(request, 'reservations/new_reservation.html', {
            'title': 'New reservation',
            'form': form,
        })
    else:#Saving reservation if everything is ok
        form = ReservationForm(request.POST)
        if form.is_valid():
            new_reservation = form.save(commit=False)
            new_reservation.user = request.user
            new_reservation.save()
            return redirect('reservations')

        else:#Exception if there is an error on fields
            return render(request, 'reservations/new_reservation.html', {
                'title': 'New reservation',
                'form': form,
                'error': 'Please check the fields carefully'
            })


# ----------------- EDIT RESERVATION -----------------
@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'GET':
        form = ReservationForm(instance=reservation)
        return render(request, 'reservations/edit_reservation.html', {
            'title': 'Edit reservation',
            'reservation': reservation,
            'form': form
        })
    else:#Saving reservation if everything is ok
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            reservation.save()
            return redirect('reservations')


# ----------------- DELETE RESERVATION -----------------
@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id, user=request.user)
    if request.method == 'POST':
        reservation.delete()
        return redirect('reservations')

    return render(request, 'reservations/reservations.html')