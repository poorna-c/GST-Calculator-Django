from django.shortcuts import render, redirect
from .forms import CreateCompanyForm, addClientForm, deleteClientForm, addMonthForm, insertForm
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Companies, Clients, Months, Records
from django.contrib.auth.decorators import login_required

# Create your views here.
selected_company = None
selected_month = None


def home(request):
    return render(request,'application/home.html',{})

@login_required
def selectCompanyView(request):
    if request.method == "POST":
        global selected_company, selected_month
        selected_company = Companies.objects.get(pk = request.POST.get('company_select'))
        selected_month = None
        return redirect('select_month_page')
    user_companies = Companies.objects.filter(user = request.user)
    return render(request,'application/selectCompany.html',{'user_companies':user_companies,'selected_company':selected_company,'selected_month':selected_month,'title':"Select Company"})

@login_required
def selectMonthView(request):
    if request.method == "POST":
        global selected_company,selected_month
        selected_month = Months.objects.get(pk = request.POST.get('month_select'))
        return redirect('insert_page')
    user_months = Months.objects.filter(company = selected_company)
    return render(request,'application/selectMonth.html',{'user_months':user_months,'selected_company':selected_company,'selected_month':selected_month,'title':"Select Month"})


@login_required
def addCompanyView(request):
    if request.method == "POST":
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            print("Form is Valid")
            a = form.save(commit=False)
            a.user = request.user
            a.save()
            messages.success(request,f"Company With Name {form.cleaned_data.get('name')} Added Successfully")
            return redirect('select_company_page')
        else:
            messages.warning(request,f"Unable to Add Company, Solve the following errors and try again")
    else:
        form = CreateCompanyForm()
    return render(request,'application/addCompany.html',{'form':form,'selected_company':selected_company,'selected_month':selected_month,'title':"Add Company"})


@login_required
def insertView(request):
    global selected_company,selected_month
    if selected_company == None:
        messages.warning(request,"Please Select Company to proceed")
        return redirect('select_company_page')
    if selected_month == None:
        messages.warning(request,"Please Select Month to proceed")
        return redirect('select_month_page')
    try:
        if request.user == selected_company.user:
            if request.method == "POST":
                form = insertForm(request.user,request.POST)
                if request.POST.get('delete')=="delete":
                    print("FORM VALID AND DELETING")
                    Records.objects.get(pk = request.POST.get('rid')).delete()
                    messages.success(request,f"Record Deleted Succesfully")
                    return redirect('insert_page')

                elif request.POST.get('update')=="update":
                    print("Update Request Recieved")
                    instance = Records.objects.get(id= request.POST.get('rid'))
                    f = insertForm(request.user,request.POST or None,instance = instance)
                    if f.is_valid():
                        print("FORM VALID AND UPDATING")
                        f.save()
                    messages.success(request,f"Record Updated Succesfully")
                    return redirect('insert_page')

                elif form.is_valid() and request.POST.get('insert')=="insert":
                    print("FORM VALID AND SAVING")
                    if form.is_valid():
                        print("FORM IS VALID")
                        a = form.save(commit = False)
                        a.month = selected_month
                        a.company = selected_company
                        a.save()
                        messages.success(request,f"Record Inserted Succesfully")
                        return redirect('insert_page')
                else:
                    messages.warning(request,f"Something Went Wrong Try Again Later")
                    messages.warning(request,f"Either Invoice already submitted.")
                    messages.warning(request,f"Negative Numbers Not Allowed. Amount Should be Positive")
                    print("Form is not VALID")
            else:
                record_ids = [str(record.id) for record in Records.objects.filter(company = selected_company,month = selected_month)]
                if request.GET.get('rid') in record_ids:
                    print("Record Found",request.GET['rid'])
                    form = insertForm(user = request.user,instance = Records.objects.get(pk=int(request.GET.get('rid'))))
                    for key in request.GET:
                        try:
                            form.fields[key].initial = request.GET[key]
                        except KeyError:
                            # Ignore unexpected parameters
                            pass
                else:
                    form = insertForm(user = request.user)
        else:
            selected_company = None
            selected_month = None
            return redirect('select_company_page')
    except:
        return redirect('select_company_page')
        
    records = Records.objects.filter(company = selected_company,month = selected_month)
    clients_details = Clients.objects.filter(company = selected_company)
    a = {}
    for c in clients_details:
        a[str(c.id)] = c.gst_no[:2]
    print(a)
    totals = {'amount':sum(map(lambda i:i.amount,records)),
    'cgst':sum(map(lambda i:i.cgst,records)),
    'sgst':sum(map(lambda i:i.sgst,records)),
    'igst':sum(map(lambda i:i.igst,records)),
    'total': sum(map(lambda i:i.total,records))
    }
    return render(request,'application/insert.html',{'form':form,'records':records,'selected_company':selected_company,'selected_month':selected_month,'totals':totals,'clients_details':a,'title':"Insert Records",'avaliable_records':len(records)})

@login_required
def addClientView(request):
    if request.method == "POST":
        form = addClientForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.company= selected_company
            a.user = request.user
            a.save()
            messages.success(request,f"Client added Successfully")
            return redirect('add_client_page')
        else:
            messages.warning(request,f"Failed to add Client")
    else:
        form = addClientForm()
        
    return render(request,'application/addClient.html',{'form':form,'selected_company':selected_company,'selected_month':selected_month,'title':"Add Client"})

@login_required
def deleteClientView(request):
    if request.method == "POST":
        print(request.POST)
        try:
            requested_client_delete = Clients.objects.get(id = request.POST.get('client'),gst_no = request.POST.get('gst_no'))
            requested_client_delete.delete()
            messages.success(request,f"Client deleted Successfully")
        except:
            messages.warning(request,"Client GST NO Doesn't match")
        return redirect('delete_client_page')
    else:
        print(selected_company,type(selected_company))
        form = deleteClientForm(user = request.user)
    return render(request,'application/deleteClient.html',{'form':form,'selected_company':selected_company,'selected_month':selected_month,'title':"Delete Client"})

@login_required
def addMonthView(request):
    if request.method == "POST":
        form = addMonthForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.company = selected_company
            a.save()
            messages.success(request,"Month Created Successfully")
            return redirect('add_month_page')
        else:
            messages.warning(request,"Error")
            return redirect('add_month_page')

        # try:
        #     m = Months(month=request.POST.get('month'),year=request.POST.get('year'),company = Companies.objects.get(id=request.POST.get('company')))
        #     m.save()
        #     messages.success(request,"Month Created Successfully")
        #     return redirect('add_month_page')
        # except:
        #     messages.warning(request,"Error")
        #     return redirect('add_month_page')
        
    else:
        form = addMonthForm()
    return render(request,'application/addMonth.html',{'form':form,'selected_company':selected_company,'selected_month':selected_month,'title':"Add Month"})
@login_required
def printView(request):
    if selected_company == None:
        return redirect('select_company_page')
    records = Records.objects.filter(company = selected_company,month=selected_month)#.order_by('-date')
    totals = {'amount':sum(map(lambda i:i.amount,records)),
    'cgst':sum(map(lambda i:i.cgst,records)),
    'sgst':sum(map(lambda i:i.sgst,records)),
    'igst':sum(map(lambda i:i.igst,records)),
    'total': sum(map(lambda i:i.total,records))
    }
    return render(request,'application/print.html',{'records':records,'company':selected_company,'month':selected_month,'totals':totals,'title':f"{selected_month}"})