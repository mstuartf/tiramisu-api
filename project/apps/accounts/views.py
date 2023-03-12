from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from ..companies.forms import CompanyForm
from ..companies.models import Company


def home_view(request):
    return render(request, 'home.html')


def signup_view(request):
    user_form = CustomUserCreationForm(request.POST)
    company_form = CompanyForm(request.POST)
    if user_form.is_valid() and company_form.is_valid():
        company = company_form.save()
        user = user_form.save()
        user.company = company
        user.save()
        return redirect('accounts:home')
    return render(request, 'signup.html', {'user_form': user_form, 'company_form': company_form})


def join_account_view(request, company_id=None):
    user_form = CustomUserCreationForm(request.POST)
    company = Company.objects.get(pk=company_id)
    if user_form.is_valid():
        user = user_form.save()
        user.company = company
        user.save()
        return redirect('accounts:home')
    return render(request, 'signup.html', {'user_form': user_form})
