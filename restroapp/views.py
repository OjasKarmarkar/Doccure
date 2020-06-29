from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth import authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth import login as loginFN
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Appointment
from datetime import datetime
import random
import string
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

# Create your views here.
CustomUser = get_user_model()


def index(request):
    if request.user.is_authenticated:
        return redirect(doctordash)
    else:
        return redirect(login)

@login_required
def docappointments(request):
    user = request.user
    if request.method == "POST":
        print(request.POST.get('status'))
        apptid = request.POST.get('ID')
        AppointmentObj = Appointment.objects.get(appointmentId = apptid)
        AppointmentObj.status = request.POST.get('status')
        AppointmentObj.save()
    appointmentList = Appointment.objects.filter(doctorMail=user.email)
    if(appointmentList.exists):
        appointmentList = appointmentList
    else:
        appointmentList = []
    Appts = {
        'doctor': user ,
        'appointments': appointmentList
    }
    return render(request , "webPages/appointments.html" , Appts)

@login_required
def doctorset(request):
    user = request.user
    pp = request.FILES.get('photo','')
    if request.method == 'POST' and pp != '':
        myfile = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        user.photo.delete()
        user.photo = filename
        user.save()
        return redirect(doctorset)
    elif request.method == "POST":
        user.first_name = request.POST.get('fname','')
        user.last_name = request.POST.get('lname','')
        user.age = request.POST.get('age','')
        user.bgroup = request.POST.get('bgroup','')
        user.age = request.POST.get('age','')
        user.email = request.POST.get('email','')
        user.phone = request.POST.get('phone','')
        user.address = request.POST.get('address','')
        user.city = request.POST.get('city','')
        user.state = request.POST.get('state','')
        user.save()
        return redirect(doctorset)
    context = {
        'user': user
    }
    return render(request, 'webPages/doctor-settings.html', context)  

@login_required
def changepassword(request):
    user = request.user
    Doctor = {
        'doctor': user,
    }
    if request.method == "POST":
        currentpassword= request.user.password
        oldpassword = request.POST.get('oldpassword', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('confirmpassword', '')
        isOldCorrect=check_password(oldpassword, currentpassword)
        if isOldCorrect :
           if password1==password2:
              user.set_password(password1)
              user.save()
              return redirect("/logout")
           else:
              return render(request, "webPages/change-password.html", Doctor)
        else:
            return render(request, "webPages/change-password.html", Doctor)      
    else:
        return render(request, "webPages/change-password.html", Doctor)
       
@login_required
def patientset(request):
    user = request.user
    pp = request.FILES.get('photo','')
    if request.method == 'POST' and pp != '':
        myfile = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        user.photo.delete()
        user.photo = filename
        user.save()
        return redirect(patientset)
    elif request.method == "POST":
        user.first_name = request.POST.get('fname','')
        user.last_name = request.POST.get('lname','')
        user.age = request.POST.get('age','')
        user.bgroup = request.POST.get('bgroup','')
        user.age = request.POST.get('age','')
        user.email = request.POST.get('email','')
        user.phone = request.POST.get('phone','')
        user.address = request.POST.get('address','')
        user.city = request.POST.get('city','')
        user.state = request.POST.get('state','')
        user.save()
        return redirect(patientset)
    context = {
        'user': user
    }
    return render(request, 'webPages/patient-settings.html', context)  

@login_required
def doctordash(request):
    if request.method == "POST":
        apptid = request.POST.get('ID')
        AppointmentObj = Appointment.objects.get(appointmentId = apptid)
        AppointmentObj.status = request.POST.get('status')
        AppointmentObj.save()
    userEmail = request.user.email
    user = CustomUser.objects.get(email=userEmail)
    appointmentList = Appointment.objects.filter(doctorMail=userEmail)
    if(appointmentList.exists):
        appointmentList = appointmentList
    else:
        appointmentList = []
    Doctor = {
        'doctor': user ,
        'appointments': appointmentList
    }
    return render(request, "webPages/doctor-dashboard.html", Doctor)

@login_required
def patientdash(request):
    userEmail = request.user.email
    appointments = Appointment.objects.filter(patientMail = userEmail)
    context = {
        'user': request.user,
        'app': appointments
    }
    return render(request, "webPages/patient-dashboard.html", context)

@login_required
def search(request):
    user = request.user
    sName = request.GET.get('name', '')
    spl = request.GET.get('spl', '')
    fields = [ x['profession'] for x in CustomUser.objects.values('profession').distinct()]
    if sName != '' and spl != '':
        doctors = CustomUser.objects.filter(is_doc=True, first_name__startswith=sName, profession=spl)
    elif sName != '':
        doctors = CustomUser.objects.filter(is_doc=True, first_name__startswith=sName)
    elif spl != '':
        doctors = CustomUser.objects.filter(is_doc=True, profession=spl)
    else:
        doctors = CustomUser.objects.filter(is_doc=True)
    
    context = {
        'doctors': doctors,
        'user': user,
        'fields': fields,
        'sName': sName,
        'spl': spl
    }
    return render(request, "webPages/search.html", context)


def signout(request):
    logout(request)
    return redirect('/login')

@login_required
def book(request):
    user = request.user
    dmail = request.GET.get('mail', '')
    try:
        doctor = CustomUser.objects.get(email=dmail)
    except:
        return HttpResponse('you shouldn\'t be here, bitch')
    context = {
        'user': user,
        'doctor': doctor
    }
    return render(request, "webPages/booking.html", context)

@login_required
def bookSuccess(request):
    user = request.user
    ip = request.GET.get('doa', '').split('/')
    dmail = request.GET.get('mail', '')
    try:
        doctor = CustomUser.objects.get(email=dmail)
    except:
        return HttpResponse('you shouldn\'t be here, bitch')
    context = {
        'user': user,
        'doctor': doctor, 
        'doa': request.GET.get('doa', '')
    }
    Appointment.objects.create(appointmentId= randomString(), doctorMail= dmail,special=doctor.profession, patientMail= user.email, patientName= user.first_name + user.last_name, doctorName= doctor.first_name + doctor.last_name,patientPhoto= user.photo, doctorPhoto= doctor.photo, dateOfAppointment= datetime(int(ip[-1]), int(ip[1]), int(ip[0])), status= "UNREVIEWED")
    return render(request, 'webPages/checkout.html', context)


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def login(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        pwd = request.POST.get('password', '')
        CustomUser = authenticate(request, email=email, password=pwd)
        loginFN(request, CustomUser)
        if CustomUser is not None:
            if(CustomUser.is_doc):
                #messages.success(request, 'Logged In Succesfully!')
                #request.session['email'] = CustomUser.email
                return redirect('/doctor')
                # return render(request, "webPages/doctor-dashboard.html" , Doctor)
            else:
               # messages.success(request, 'Logged In Succesfully!')
                #request.session['email'] = CustomUser.email
                return redirect('/patient')
        else:
            return HttpResponse("<h1>Login Not</h1>")
    #username = request.POST['username']
    #password = request.POST['password']

    return render(request, "webPages/login.html")


def register(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        pwd = request.POST.get('password', '')
        fname = request.POST.get('fname', '')
        lname = request.POST.get('lname', '')
        user = CustomUser.objects.create_user(
            email=email, password=pwd, first_name=fname, last_name=lname)
        if user is not None:
            #messages.success(
                #request, 'Account Created Successfully , Please Login Again!')
            response = redirect('/login')
            return response
        else:
            #messages.error(request, 'Error Creating Account')
            return HttpResponse("<h1>Register Not</h1>")
    return render(request, "webPages/register.html")
