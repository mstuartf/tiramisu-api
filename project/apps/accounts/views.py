from django.shortcuts import render, redirect
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .forms import CustomUserCreationForm
from .serializers import ReadUserSerializer
from ..companies.forms import CompanyForm
from ..companies.models import Company
from .models import CustomUser


def signup_success_view(request):
    return render(request, 'signup_success.html')


def signup_view(request):
    user_form = CustomUserCreationForm(request.POST)
    company_form = CompanyForm(request.POST)
    if user_form.is_valid() and company_form.is_valid():
        company = company_form.save()
        user = user_form.save()
        user.company = company
        user.admin = True
        user.save()
        return redirect('accounts:signup_success')
    return render(request, 'signup.html', {'user_form': user_form, 'company_form': company_form})


def join_account_view(request, company_id=None):
    user_form = CustomUserCreationForm(request.POST)
    company = Company.objects.get(pk=company_id)
    if user_form.is_valid():
        user = user_form.save()
        user.company = company
        user.save()
        return redirect('accounts:signup_success')
    return render(request, 'signup.html', {'user_form': user_form})


class UserView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):

    serializer_class = ReadUserSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(
            company=self.request.user.company
        )

    def get_object(self):
        pk = self.kwargs['pk']
        if pk == 'me':
            return self.request.user
        else:
            return super().get_object()
