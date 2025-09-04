from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User

# ----------------- PROMOTERS -----------------
class PromoterForm(forms.ModelForm):
    class Meta:
        model = Promoter
        fields = ['first_name', 'last_name', 'area', 'phone']
        labels = {
            'first_name': 'Name',
            'last_name': 'Surname',
            'area': 'Assigned area',
            'phone': 'Contact phone',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
            'area': forms.TextInput(attrs={}),
            'phone': forms.NumberInput(attrs={}),
        }


# ----------------- SEARCH PROMOTER -----------------
class SearchPromoterForm(forms.Form):
    b_promoter = forms.CharField(
        label='Search promoter',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'search-field', 'placeholder':'Enter promoter hint'})
    )


# ----------------- CUSTOMERS -----------------
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'city', 'nationality', 'phone', 'email', 'promoter']
        labels = {
            'first_name': 'Name',
            'last_name': 'Last Name',
            'address': 'Address',
            'city': 'City',
            'nationality': 'Nationality',
            'phone': 'Phone',
            'email': 'Email',
            'promoter': 'Promoter',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={}),
            'last_name': forms.TextInput(attrs={}),
            'address': forms.TextInput(attrs={}),
            'city': forms.TextInput(attrs={}),
            'nationality': forms.Select(attrs={}),
            'phone': forms.NumberInput(attrs={}),
            'email': forms.EmailInput(attrs={}),
            'promoter': forms.Select(attrs={}),
        }


# ----------------- SEARCH CUSTOMER -----------------
class SearchCustomerForm(forms.Form):
    b_customer = forms.CharField(
        label='Search customer',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'search-field', 'placeholder':'Enter customer hint'})
    )


# ----------------- TABLES -----------------
class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity', 'price']
        labels = {
            'number': 'Number',
            'capacity': 'Capacity',
            'price': 'Price',
        }
        widgets = {
            'number': forms.NumberInput(attrs={'class':'form-control'}),
            'capacity': forms.NumberInput(attrs={'class':'form-control'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
        }


# ----------------- RESERVATIONS -----------------
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer', 'table', 'guests', 'date', 'promoter']
        labels = {
            'customer': 'Customer',
            'table': 'Table number',
            'guests': 'Guests',
            'date': 'Date',
            'promoter': 'Promoter',
        }
        widgets = {
            'customer': forms.Select(attrs={'class':'form-control'}),
            'table': forms.Select(attrs={'class':'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'promoter': forms.Select(attrs={'class':'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        guests = cleaned_data.get('guests')

        if table and guests:#Exception if user want to put more guests than the table admits
            if guests > table.capacity:
                raise ValidationError(
                    f'The reservation exceeds the available capacity at table No.{table.number} ({table.capacity})'
                )
        return cleaned_data


# ----------------- SEARCH RESERVATION BY ANY HINT-----------------
class SearchReservationForm(forms.Form):
    b_reservation = forms.CharField(
        label='Search reservation',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'search-field', 'placeholder':'Enter a reservation hint'})
    )


# ----------------- SEARCH RESERVATION BY DATE -----------------
class ReservationDateForm(forms.Form):
    start_date = forms.DateField(label='Start date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))


# ----------------- EDIT PROFILE -----------------
class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=100, label="Username")
    first_name = forms.CharField(max_length=100, label="Name")
    last_name = forms.CharField(max_length=100, label="Surname")
    email = forms.EmailField(label="Email")

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New password'}),
        label="New password", required=False
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'}),
        label="Confirm password", required=False
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords do not match')
        return cleaned_data