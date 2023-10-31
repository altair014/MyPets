from typing import Any
from django import forms
from django.forms import Form, ModelForm, ValidationError

# create your forms here

from pets_app.models import PetInformation, PetServices, OwnerModel, CountryModel

from django.contrib.auth.models import User

class UserLogup(Form):
    text_dict = forms.TextInput(attrs={'class':'form-control my-2 w-auto'})
    pass_dict = forms.PasswordInput(attrs={'class':'form-control my-2 w-auto'})
    email_dict = forms.EmailInput(attrs={'class':'form-control my-2 w-auto'})

    first_name = forms.CharField(max_length=20, widget=text_dict, label='First Name', required=False)
    last_name = forms.CharField(max_length=20, widget=text_dict, label='Last Name', required=False)
    email = forms.EmailField(max_length=30, widget=email_dict, initial='some@domain.com')
    username = forms.CharField(max_length=10, widget=text_dict)
    passphrase = forms.CharField(max_length=32, widget=pass_dict)
    admin = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input', 'onclick':'myFunction()'}))
    key = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class':'form-control my-2 w-auto', 'hidden':'true'}))

    def clean(self):
        req_user = self.cleaned_data.get('username')

        try:
            user= User.objects.get(username=req_user)
        except User.DoesNotExist:
            user = None
            
        if user:
            raise ValidationError(f"Username '{req_user}' already exists.")
        
class UserLogin(Form):
    username = forms.CharField(max_length=10, widget= UserLogup.text_dict)
    passphrase = forms.CharField(max_length=32, widget=UserLogup.pass_dict)

    def clean(self):
        req_user = self.cleaned_data.get('username')
        req_pass = self.cleaned_data.get('passphrase')

        try:
            user = User.objects.get(username=req_user)
        except User.DoesNotExist:
            raise ValidationError('Incorrect Username.')
        
        if user.check_password(raw_password=req_pass):
            return self.cleaned_data
        raise ValidationError('Incorrect password.')

    # def clean_username(self):
    #     # cleaned_data = super().clean()
    #     req_user = self.cleaned_data.get('username')

    #     user_data = User.objects.all()

    #     for item in user_data:
    #         if req_user == item.username:
    #             return req_user

    #     raise ValidationError(message='Incorrect Username')

class CountryModelForm(ModelForm):
    class Meta:
        model=CountryModel
        fields='__all__'

        widgets={
                "country_code":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
                "country_name":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
        }

        labels={
                "country_name":"Name",
                "country_code":"Country_Code",
        }

class OwnerModelForm(ModelForm):
    class Meta:
        model=OwnerModel
        fields='__all__'
        exclude = ('created_by', 'updated_by')

        widgets={
                "owner_name":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
                "owner_contact_prefix":forms.Select(attrs={'class':'form-select my-2 w-auto'}),
                "owner_contact":forms.NumberInput(attrs={'class':'form-control my-2 w-auto'}),
                "owner_date":forms.DateInput(attrs={'class':'form-control my-2 w-auto'}),
                "owner_city":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
                "owner_state":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
                "owner_country":forms.TextInput(attrs={'class':'form-control my-2 w-auto' }),
        }

        labels={
                "owner_name":"Name",
                "owner_contact_prefix":"Contact Prefix",
                "owner_contact":"Contact",
                "owner_date":"Date",
                "owner_city":"City",
                "owner_state":"State",
                "owner_country":"Country",
        }
        
class PetInformationForm(ModelForm):
    class Meta:
        model = PetInformation
        fields = '__all__'
        exclude = ('owner','created_by', 'updated_by')
        
        widgets = {
                    'name':forms.TextInput(attrs={'class':'form-control my-2 w-auto' }), 
                    'pet_type':forms.Select(attrs={'class':'form-select my-2 w-auto'}),
                    'age':forms.NumberInput(attrs={'class':'form-control my-2 w-auto'}),
                    'breed':forms.Select(attrs={'class':'form-select my-2 w-auto'}),
                    'gender':forms.Select(attrs={'class':'form-select my-2 w-auto'}),
                    'weight':forms.NumberInput(attrs={'class':'form-control my-2 w-auto'}),
                    'image':forms.FileInput(attrs={'class':'form-control mt-4 mb-2 w-auto'}),
                    }
        labels = {
                    'name':'Pet Name',
                    'pet_type':'Pet Type',
                    'breed':'Breed',
                    'age':'Age ', 
                    'gender': 'Gender ',
                    'weight':'Weight ',
                    'image':'',
        }
 
    def clean(self):
        req_weight = self.cleaned_data.get('weight')
        req_age = self.cleaned_data.get('age')

        if int(req_age) <= 0:
            raise ValidationError(message='Age cannot be less than or equal to zero.')
        if int(req_weight) <= 0:
            raise ValidationError(message='Weight cannot be less than or equal to zero.')
    
class PetServicesForm(ModelForm):
    class Meta:
        model = PetServices
        fields = ['service_required','grooming_type','consultation_type']
        widgets = {
            'service_required':forms.Select(attrs={'class':'form-select my-2 w-auto','onchange':'myFunction()'}),
            'grooming_type':forms.Select(attrs={'class':'form-select my-2 w-auto', 'hidden':'true'}),
            'consultation_type':forms.Select(attrs={'class':'form-select my-2 w-auto', 'hidden':'false', 'required':'true'}),
            }
        labels = {
            'service_required': 'Service Required',
            'grooming_type': 'Grooming Type',
            'consultation_type': 'Consultation Type'
            }