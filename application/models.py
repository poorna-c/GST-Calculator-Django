from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator


class Companies(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length = 64,unique=True)
    gst_no = models.CharField(max_length = 15,unique=True,validators=[MinLengthValidator(15),MaxLengthValidator(15)])

    def __str__(self):
        return str(self.name)

class Clients(models.Model):
    company = models.ForeignKey(Companies,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    gst_no = models.CharField(max_length = 15,validators=[MinLengthValidator(15)])
    default_hsn = models.CharField(max_length=15, blank = True,null = True)
    def __str__(self):
        return str(self.name)
    class Meta:
        unique_together = ('company','gst_no')

class Months(models.Model):
    month = models.CharField(max_length = 3)
    year = models.CharField(max_length = 4,validators=[MinLengthValidator(4)])
    company = models.ForeignKey(Companies,on_delete = models.CASCADE)
    def __str__(self):
        return str(self.month) + ' ' + str(self.year) + ' ' + str(self.company)
    class Meta:
        unique_together = ('month','year','company')


class Records(models.Model):
    month = models.ForeignKey(Months,on_delete = models.CASCADE)
    client = models.ForeignKey(Clients,on_delete = models.CASCADE)
    company = models.ForeignKey(Companies,on_delete = models.CASCADE)
    date = models.DateField()
    hsn_code = models.CharField(max_length = 15, blank =True,null = True)
    invoice = models.CharField(max_length = 15, blank =True,null = True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    # amount = models.FloatField(validators=[MinValueValidator(0)])
    percentage = models.FloatField(default = 5.0)
    cgst = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    sgst = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    igst = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    total = models.DecimalField(max_digits=10,decimal_places=2,validators=[MinValueValidator(0)])
    # cgst = models.FloatField(validators=[MinValueValidator(0)])
    # sgst = models.FloatField(validators=[MinValueValidator(0)])
    # igst = models.FloatField(validators=[MinValueValidator(0)])
    # total = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.client.name)+ ' ' + str(self.date)+ ' ' + str(self.invoice)
    class Meta:
        unique_together = ('client','invoice')

    # def save(self, *args, **kwargs):
    #     self.cgst = round(self.cgst, 2)
    #     self.sgst = round(self.sgst, 2)
    #     self.igst = round(self.igst, 2)
    #     self.total = round(self.total, 2)
    #     self.amount = round(self.amount, 2)
    #     super().save(*args, **kwargs)