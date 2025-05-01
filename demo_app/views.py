# from django.shortcuts import render

# Create your views here.
from contextvars import Token
import datetime
from email import message
import json
from pyexpat.errors import messages

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from demo_app.serializers import ProfileSerializer, registerSerializer
from .models import MedicineLog, register
from rest_framework import generics

from django.contrib.auth.hashers import check_password
# Replace with the correct import path for your 'register' model

from django.contrib.auth import authenticate, login,logout


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.shortcuts import render, redirect
from django.contrib import messages


from django.http import JsonResponse

def check_user_session(request):
    return JsonResponse({
        "authenticated": request.user.is_authenticated,
        "user": request.user.email if request.user.is_authenticated else "None"
    })
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to access this page.")
            return redirect('login')  
        return view_func(request, *args, **kwargs)
    return wrapper

@custom_login_required
def homepage(request):
    print(request.session.items())  

    return render(request,'home.html')

def hello(request):
    return render(request,'idk.html')
from .models import MedicineLog
from datetime import date, timedelta
@custom_login_required
def schedule(request):
    
    if request.method == "POST":
        medicine_name = request.POST.get("medicine_name")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        schedule_times = request.POST.getlist("schedule[]")  # Morning/Afternoon/Night

        if medicine_name and start_date and end_date:
            for time in schedule_times:
                MedicineLog.objects.create(
                    user=request.user,  # Ensure user is authenticated
                    medicine_name=medicine_name,
                    start_date=start_date,
                    end_date=end_date,
                    time=time
                )
        return redirect("schedule")  


    medicine_logs = MedicineLog.objects.filter(user=request.user).order_by("start_date")

    return render(request, "schedule.html", {"medicine_logs": medicine_logs})
    

  
    
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import MedicineLog
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import MedicineLog, MedicineStatus
from django.utils.dateparse import parse_date

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import MedicineLog, MedicineStatus,Profile



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import MedicineStatus, MedicineLog

def update_medication_status(request):
  
    try:
        data = json.loads(request.body)  
        print(data, "data")
        medicine_name = data.get("medicine_name")
        date = data.get("date")
        status = data.get("status")
        print(date, "This is the date")
        # Ensure all required fields are present
        if not medicine_name or not date or not status:
            return JsonResponse({"success": False, "error": "Missing required fields"}, status=400)

        
        # date = datetime.strptime(date, "%Y-%m-%d").date()

        try:
            medicine_log = MedicineLog.objects.filter(medicine_name = medicine_name).first()
            print(medicine_log, "Thi is a medicine log")
        except MedicineLog.DoesNotExist:
            print("Thi is an error")
            return JsonResponse({"success": False, "error": "MedicineLog not found"}, status=404)

        # Update or create MedicineStatus entry
        log, created = MedicineStatus.objects.update_or_create(
            medicine_log=medicine_log,
            date=date,
            defaults={"status": status}
        )

        return JsonResponse({"success": True, "message": "Medicine status updated successfully"})

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON format"}, status=400)

    except ValueError:
        return JsonResponse({"success": False, "error": "Invalid date format"}, status=400)

from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import UploadedFile
@custom_login_required
def testresult(request):
    if request.method == 'POST' and request.FILES.get('file'):

        uploaded_file = request.FILES['file']
        fs = FileSystemStorage(location=settings.MEDIA_ROOT) 
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

    
        file_instance = UploadedFile(
        user=request.user,  
        file=filename
    )
        file_instance.save()
    uploaded_files = UploadedFile.objects.filter(user=request.user)

    return render(request, 'main.html', {'uploaded_files': uploaded_files})



from django.contrib import messages  
from django.shortcuts import redirect


from django.http import JsonResponse
from .models import UploadedFile


def get_uploaded_files(request):
    files = UploadedFile.objects.all() 
    file_data = []
    for file in files:
        file_data.append({
            'name': file.file.name,
            'file_url': file.file.url,
        })
    return JsonResponse({'files': file_data})



@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    
        user = authenticate(request, username=email, password=password)  

        if user is not None:
            login(request, user) 
            return redirect("home")  
        
        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html', {'error': 'Invalid credentials. Please try again.'})
    return render(request, 'login.html', {'error': None})

from django.shortcuts import redirect, render

def register_view(request):
   
    return render(request, 'register.html', {'error': None})

from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
@api_view(['POST'])
@permission_classes([AllowAny]) 
def manage_register(request):
    if request.method=='POST':
        serializer=registerSerializer(data=request.data)  #storing,mapping the data in the variable and then checking it 
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
           
        else:
              return render(request, 'register.html', {'error': serializer.errors})
    
    return render(request, 'register.html', {'error': None})


def custom(request):
    logout(request)

    return redirect('login')


def profile_view(request):
   return render(request,'profile.html')
   
@csrf_exempt
@custom_login_required
@api_view(['POST'])
def profile(request):
    if request.method=='POST':
        print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

        serializer=ProfileSerializer(data=request.data,context={'request': request}) 
        
      
        if serializer.is_valid():
            print("som")
            serializer.save()
            return redirect('profile')
          
        else:
              return render(request, 'profile.html', {'error': serializer.errors})
    
    return render(request, 'profile.html', {'error': None})
@custom_login_required  
def get_profiles(request):
    try:
        print("fetching")
        profile = Profile.objects.get(user=request.user)  

        profile_data = {
            'full_name': profile.full_name,
            'phone_number': profile.phone_number,
            'birth_date': profile.birth_date.strftime("%Y-%m-%d") if profile.birth_date else None,
            'gender': profile.gender,
            'blood_group': profile.blood_group,
        }

        return JsonResponse({'profile': profile_data}) 

    except Profile.DoesNotExist:
        
        return JsonResponse({"error": "Profile not found"}, status=404)


def get_taken_status(request):
    taken_statuses = MedicineStatus.objects.filter(status="taken")  
    print("Hello")
    taken_dates = [
        {
            "medicine_name": entry.medicine_log.medicine_name,
            "date": entry.date.strftime("%Y-%m-%d")
        }
        for entry in taken_statuses
    ]

    
    return JsonResponse({"taken_dates": taken_dates})  

from django.http import JsonResponse
from .tasks import send_email_task

from django.http import HttpResponse
from demo_app.tasks import send_email_task

def send_email_view(request):
    send_email_task.delay(
        "Test Email from Celery",
        "This is a test email sent using Celery.",
        ["p.kalash017@example.com"],  # Replace with recipient's email
    )
    return HttpResponse("Email is being sent in the background!")
