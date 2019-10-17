from django import forms
from .models import Companies, Clients, Months, Records
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator,MaxLengthValidator

# class SelectCompanyForm(forms.Form):
#     select_company = forms.ModelChoiceField(None)
#     class Meta:
#         model = Companies
#         fields = ['select_company']
#     def __init__(self, user, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['select_company'].queryset = Companies.objects.filter(user=user)

class CreateCompanyForm(forms.ModelForm):
    gst_no = forms.CharField(max_length = 15,min_length=15)
    class Meta:
        model = Companies
        fields = ['name','gst_no']
    

class addClientForm(forms.ModelForm):
    class Meta:
        model = Clients
        fields = ['name','gst_no','default_hsn']


class deleteClientForm(forms.ModelForm):
    client = forms.ModelChoiceField(None)
    gst_no = forms.CharField(max_length=15)
    class Meta:
        model = Clients
        fields = ['client','gst_no']
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Clients.objects.filter(user=user)


class addMonthForm(forms.ModelForm):
    CHOICE_FIELDS = (
        ('---','--------'),
        ('JAN','JANUARY'),
        ('FEB','FEBUARY'),
        ('MAR','MARCH'),
        ('APR','APRIL'),
        ('MAY','MAY'),
        ('JUN','JUNE'),
        ('JLY','JULY'),
        ('AUG','AUGUST'),
        ('SEP','SEPTEMBER'),
        ('OCT','OCTOBER'),
        ('NOV','NOVEMBER'),
        ('DEC','DECEMBER'),
    )
    years = [('----','----')]
    i = 0
    for i in range(2018,2050):
        years.append((str(i),str(i)))
    years = tuple(years)
    month = forms.ChoiceField(choices = CHOICE_FIELDS)
    year = forms.ChoiceField(choices = years)
    #company = forms.ModelChoiceField(None)
    class Meta:
        model = Months
        fields = ['month','year']#,'company']

    # def __init__(self, user, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['company'].queryset = Companies.objects.filter(user=user)

class insertForm(forms.ModelForm):
    # month = forms.ModelChoiceField(Months.objects.all(),widget=forms.Select(attrs={'readonly':'readonly'}))
    rid = forms.CharField(max_length=10,required=False,label="ID",widget=forms.TextInput(attrs={'readonly':'readonly'}))
    date = forms.DateField(widget = forms.TextInput(attrs={'type':'date'}))
    # gst_no = forms.CharField(initial = 0)
    #month = forms.ModelChoiceField(Months.objects.all(),widget = forms.Select(attrs={'disabled':'disabled'}))
    amount = forms.DecimalField(max_digits=10,decimal_places=2)
    cgst = forms.DecimalField(max_digits=10,decimal_places=2,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    sgst = forms.DecimalField(max_digits=10,decimal_places=2,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    igst = forms.DecimalField(max_digits=10,decimal_places=2,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    total = forms.DecimalField(max_digits=10,decimal_places=2,widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # cgst = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # sgst = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # igst = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # total = forms.FloatField(widget = forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = Records
        fields = ['rid','date','client','hsn_code','invoice','amount','percentage','cgst','sgst','igst','total']
    def __init__(self,user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = Clients.objects.filter(user = user).order_by('name')


        
    
