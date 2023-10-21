from django.contrib import admin
from django.contrib.admin import ModelAdmin, site

# Register your models here.

from pets_app.models import PetInformation

class PetInformationAdmin(ModelAdmin):
    fields = ['name', 'pet_type', 'age', 'gender', 'weight', 'owner']

site.register(PetInformation, PetInformationAdmin)