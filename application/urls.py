from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home_page"),
    path('selectcompany.html',views.selectCompanyView,name="select_company_page"),
    path('selectmonth.html',views.selectMonthView,name="select_month_page"),
    path('addcompany.html',views.addCompanyView,name = "add_company_page"),
    path('insert.html',views.insertView,name = "insert_page"),
    path('addclient.html',views.addClientView,name = "add_client_page"),
    path('deleteclient.html',views.deleteClientView,name = "delete_client_page"),
    path('addmonth.html',views.addMonthView,name="add_month_page"),
    path('print.html',views.printView,name="print_page"),
    
    #path('ajax/loadmonths/',views.loadMonthsView,name="load_months_url")
]