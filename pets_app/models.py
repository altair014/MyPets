from django.db import models
from django.db.models import Model
from django.urls import reverse

# Create your models here.

class CountryModel(Model):
    country_code = models.CharField(max_length=5, unique=True, primary_key=True)
    country_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.country_code}"

class OwnerModel(Model):
    owner_name = models.CharField(max_length=30)
    owner_contact_prefix = models.ForeignKey(to=CountryModel, on_delete=models.PROTECT, to_field='country_code')
    owner_contact = models.PositiveIntegerField(unique=True)    
    owner_date = models.DateField(auto_created=True, auto_now_add=True)
    owner_city = models.CharField(max_length=30, default='Bengaluru')
    owner_state = models.CharField(max_length=30, default='Karnataka')
    owner_country = models.CharField(max_length=30, default='India')

    def get_absolute_url(self):
        return reverse(viewname='pets_app_name:owner_detail_name', kwargs={'pk':self.pk}) 
    
    def __str__(self):
        return f"{self.owner_contact_prefix} {self.owner_contact}"

class PetInformation(Model):
    class PetType(models.TextChoices):
        CAT = "Cat", "Cat"
        DOG = "Dog", "Dog"
        HORSE = "Horse", "Horse"
        RABBIT = "Rabbit", "Rabbit"
        PIGEON = "Pigeon", "Pigeon"

    class PetGender(models.TextChoices):
        Male = "M", "Male"
        Femail = "F", "Female"
        Unknown = "Unknown","Unknown"

    class Breed(models.TextChoices):
        German_Shephard = "German_Shephard", "German_Shephard"
        Labrador = "Labrador", "Labrador"
        Indie = "Indie", "Indie"
        Persian = "Persian", "Persian"

    date = models.DateField(auto_created=True, auto_now_add=True)
    name = models.CharField(max_length=30)
    age = models.PositiveSmallIntegerField()
    pet_type = models.CharField(max_length=10, choices=PetType.choices, default=PetType.CAT)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    breed = models.CharField(max_length=20, choices=Breed.choices, default=Breed.Indie)
    gender = models.CharField(max_length=7, choices=PetGender.choices, default=PetGender.Male)
    image = models.ImageField(upload_to='images/', blank=True)
    contact = models.ForeignKey(to=OwnerModel, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse(viewname='pets_app_name:pet_detail_name', kwargs={'pk':self.pk})    

class PetServices(Model):
    class PetServiceType(models.TextChoices):
        GROOMING = 'Grooming','Grooming'
        CONSULTATION = 'Consultation','Consultation'
        BOTH = 'Both'+'Both'

    class Grooming(models.TextChoices):
        HAIR_CUTTING = 'Hair Cutting', 'Hair Cutting'
        HAIR_CLEANING = 'Hair Cleaning', 'Hair Cleaning'
        BODY_WASH = 'Body Wash', 'Body Wash'
        NAIL_CLEANING = 'Nail Cleaning', 'Nail Cleaning'
        NAIL_CUTTING = 'Nail Cutting', 'Nail Cutting'   

    class Consultaion(models.TextChoices):
       DOCTOR_1 = 'Doctor 1', 'Doctor 1'
       DOCTOR_2 = 'Doctor 2', 'Doctor 2'
       DOCTOR_3 = 'Doctor 3', 'Doctor 3'
       DOCTOR_4 = 'Doctor 4', 'Doctor 4'

    service_required = models.CharField(max_length=20, choices=PetServiceType.choices, default=PetServiceType.CONSULTATION)
    grooming_type = models.CharField(max_length=20, choices=Grooming.choices, blank=True)
    consultation_type = models.CharField(max_length=20, choices=Consultaion.choices, blank=True)
    date = models.DateField(auto_created=True, auto_now_add=True)
    time = models.TimeField(auto_created=True, auto_now_add=True)
    pet_name = models.CharField(max_length=10, blank=True)
    contact = models.PositiveIntegerField(blank=True)
    id_2 = models.PositiveBigIntegerField(blank=True)
