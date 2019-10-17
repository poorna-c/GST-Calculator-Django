from django.contrib import admin
from .models import Companies,Clients,Months, Records
# Register your models here.
admin.site.register(Companies)
admin.site.register(Clients)
admin.site.register(Months)
admin.site.register(Records)
