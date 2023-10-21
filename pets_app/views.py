from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from django.urls import reverse_lazy, reverse

from django.views.generic import View, TemplateView, RedirectView, CreateView, FormView, ListView, DetailView, UpdateView, DeleteView

# Create your views here.

from pets_app.models import PetInformation, PetServices, OwnerModel, CountryModel

from pets_app.forms import UserLogin, UserLogup, PetInformationForm, PetServicesForm, OwnerModelForm, CountryModelForm

from pets_app.mixins import SomeLoginRequiredMixin, SomePermissionRequiredMixin

from django.contrib.auth import authenticate, login, logout, user_logged_in

from django.contrib.messages import info, success, error, get_messages

from django.contrib.auth.models import User

from random import randrange, randint

from time import sleep

class PetsView(TemplateView):
    template_name = 'pets.html'
    
class UserCreateView(FormView):
    form_class = UserLogup
    template_name = 'pets_app/userlogup.html'
    success_url = reverse_lazy('pets_app_name:user_login_name')

    _admin_key = str(randrange(999999,2147483646,(randint(1,9)))) #for now later will be replaced by o-auth or jwt-auth
    _staff_key = str(randrange(999999,2147483646,(randint(1,9)))) #for now later will be replaced by o-auth or jwt-auth

    def get(self, request, *args, **kwargs):
        info(request=request, message='Please provide your credentials.')
        print(f'{self._admin_key}\n{self._staff_key}')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        data_name = form.cleaned_data
        user_name = data_name['username']
        pass_name = data_name['passphrase']
        email_name = data_name['email'] 
        ad_min = data_name.get('admin', None)
        key = data_name.get('key', None)

        if self.get_form().is_valid():
            if ad_min and key == self._admin_key:                
                User.objects.create_superuser(username= user_name, email= email_name, password= pass_name,first_name=data_name['first_name'], last_name=data_name['last_name'])
            elif ad_min and key == self._staff_key:
                User.objects.create_superuser(username= user_name, email= email_name, password= pass_name,first_name=data_name['first_name'], last_name=data_name['last_name'])
                sleep(5)
                User.objects.filter(username=user_name).update(is_staff=0)
            else:
                User.objects.create_user(username= user_name, email= email_name, password= pass_name,first_name=data_name['first_name'], last_name=data_name['last_name'])
            return super().form_valid(form=form)
        else:
            return super().form_invalid(form=form)

class UserLoginFormView(FormView):
    form_class = UserLogin
    template_name = 'pets_app/userlogin.html' 
    
    def get(self, request, *args, **kwargs):            
        if len(get_messages(request=request)) == 0 and not request.user.is_authenticated:
            info(request=request, message='Please provide your credentials.')
        else:
            logout(request=request)
            success(request=request, message='You have successfully logged out. Please provide your credentials to login again.')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_user = request.POST.dict()['username']
        request_pass = request.POST.dict()['passphrase']

        user = authenticate(username=request_user, password=request_pass)

        if user is not None:
            login(request=request, user=user)
            success(request=request, message='You have successfully logged in.')
            if self.request.GET.get('next') == None :
                return redirect(reverse(viewname='pets_app_name:owner_list_name'))
            return redirect(self.request.GET.get('next'))  # Redirect to a protected page
        
        return self.form_invalid(form=self.get_form())
    
class OwnerCreateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, CreateView):
    model = OwnerModel
    form_class = OwnerModelForm
    success_url = reverse_lazy('pets_app_name:pet_create_name')
    permission_required = 'pets_app.add_ownermodel'

    def get(self, request, *args, **kwargs):
        if len(CountryModel.objects.all())==0:
            CountryModel.objects.create(country_name='IND', country_code='+91')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form_data = form.cleaned_data
        try:
            OwnerModel.objects.get(**form_data)
        except OwnerModel.DoesNotExist:
            return super().form_valid(form)
        return super().form_invalid(form)

class OwnerListView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, ListView):
    model = OwnerModel
    permission_required = 'pets_app.view_ownermodel'

class OwnerDetailView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DetailView):
    model = OwnerModel
    permission_required = 'pets_app.view_ownermodel'

class OwnerUpdateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, UpdateView)        :
    model = OwnerModel
    form_class = OwnerModelForm
    template_name = 'pets_app/owner_update_form.html'
    permission_required = 'pets_app.change_ownermodel'
    
class OwnerDeleteView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DeleteView):
    model = OwnerModel
    success_url = reverse_lazy('pets_app_name:owner_list_name')
    permission_required = 'pets_app.delete_ownermodel'

class PetInformationCreateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, CreateView):
    model = PetInformation
    form_class = PetInformationForm
    permission_required = 'pets_app.add_petinformation'

    def get_success_url(self):
        success_url = '/pets/pet_list_route/' + str(self.request.POST.get('contact'))
        return success_url

    def post(self, request, *args, **kwargs):
        petinfo_form = PetInformationForm(self.request.POST, self.request.FILES)
           
        if petinfo_form.is_valid():
            pet_data = petinfo_form.cleaned_data
            pet_data.pop('image')            
            print(pet_data)
            try:
                PetInformation.objects.get(**pet_data)
            except PetInformation.DoesNotExist:
                petinfo_form.save(commit=True)
                success(request=self.request, message=f'''A new pet record with the name "{petinfo_form.cleaned_data.get('name').capitalize()}" has been created successfully.''')
            sleep(3)            
            return redirect(to=self.get_success_url())
 
        return super().form_invalid(form=petinfo_form)

class PetListView(SomeLoginRequiredMixin, ListView):
    model = PetInformation
    permission_required = 'pets_app.view_petinformation'


    def get(self, request, contact, *args, **kwargs):
        pets = PetInformation.objects.all().filter(contact=contact)
        s_no = []
        for item in range(len(pets)):
            print(item)
            s_no.append(item+1)
        try:
            queryset = PetInformation.objects.all().filter(contact=contact)
        except PetInformation.DoesNotExist:
            queryset = PetInformation.objects.all()
        return render(request=request, template_name='pets_app/petinformation_list.html', context={'object_list':queryset, 's_no':s_no})


class PetDetailView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DetailView):
    model = PetInformation
    permission_required = 'pets_app.view_petinformation'
    
    def get(self, request, pk, *args, **kwargs):
        petinformation = PetInformation.objects.get(id=pk)
        petservice = PetServices.objects.filter(pet_name=petinformation.name, contact=petinformation.contact.owner_contact, id_2=pk)
        return render(request=request, template_name='pets_app/petinformation_detail.html', context={'petinformation':petinformation, 'petservice':petservice})

class PetUpdateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, UpdateView):
    model = PetInformation
    form_class = PetInformationForm
    template_name = 'pets_app/pet_update_form.html'
    permission_required = 'pets_app.change_petinformation'

    def form_valid(self, form):
        if form.has_changed():
            success(request=self.request, message=f'''The record with the name "{form.cleaned_data.get('name')}" record has been updated successfully.''')
        else:
            info(request=self.request, message='No changes has been performed.')
        return super().form_valid(form)

class PetDeleteView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DeleteView):
    model = PetInformation
    permission_required = 'pets_app.delete_petinformation'

    def post(self, request, pk, *args, **kwargs):
        contact= (PetInformation.objects.get(id=pk).contact.owner_contact)
        PetInformation.objects.get(id=pk).delete()
        PetServices.objects.filter(id_2=pk).delete()
        return redirect(to='/pets/pet_list_route/'+str(contact))
    
class ServiceCreateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, CreateView):
    model = PetServices
    form_class = PetServicesForm
    permission_required = 'pets_app.add_petservices'

    def post(self, request, *args, **kwargs):
        service_form = PetServicesForm(self.request.POST)
           
        if service_form.is_valid():
            service_data = service_form.cleaned_data
            identity = ''
            for item in self.request.GET.get('next'):
                if item.isdigit():
                    identity = identity+item
            identity = int(identity)
            test = PetInformation.objects.get(id=identity)
            contact = test.contact.owner_contact
            number = test.pk
            name = test.name
            service_data.update({'id_2':number, 'contact':contact, 'pet_name':name})
            print(service_data)
            PetServices.objects.create(**service_data)
            # try:
            #     PetInformation.objects.get(**pet_data)
            # except PetInformation.DoesNotExist:
            #     petinfo_form.save(commit=True)
            sleep(2)            
            return redirect(to=self.request.GET.get('next'))
 
        return super().form_invalid(form=service_form)

class ServiceListView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, ListView):
    model = PetServices
    permission_required = 'pets_app.view_petservices'


class ServiceDetailView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DetailView):
    model = PetServices
    permission_required = 'pets_app.view_petservices'

class ServiceUpdateView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, UpdateView):
    model = PetServices
    permission_required = 'pets_app.change_petservices'

class ServiceDeleteView(SomeLoginRequiredMixin, SomePermissionRequiredMixin, DeleteView):
    model = PetServices
    permission_required = 'pets_app.delete_petservices'

