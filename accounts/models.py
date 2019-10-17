from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from PIL import Image

User._meta.get_field('email')._unique = True

# Create your models here.

class profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    image = models.ImageField(default = 'default.jpg',upload_to = 'profile_pics')
    date_of_birth = models.DateField(blank = True,null = True)
    website= models.URLField(max_length=250,blank = True, null = True)
    github= models.URLField(max_length=250,blank = True, null = True)
    linked_in= models.URLField(max_length=250,blank = True, null = True)
    bio = models.TextField(max_length = 256,blank = True, null = True)
    first_login_ip = models.GenericIPAddressField(blank = True,null = True)
    phone_number = PhoneNumberField(blank = True,null =True)
    phone_number2 = PhoneNumberField(blank = True,null =True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default = 'M')

    def __str__(self):
        return self.user.username + ' Profile'

    #def save(self):
    #    super().save()
    #    img = Image.open(self.image.path)

    #    if img.height > 256 or img.width > 256:
    #        output_size = (256,256)
    #        img.thumbnail(output_size)
    #        img.save(self.image.path)





