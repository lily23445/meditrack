from django.urls import path
from . import views
from demo_app.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("send-email/", send_email_view, name="send_email"),
    path('register',views.register_view,name="register"),
    # path('login',views.login_view,name="login"),
    path('registerAPI', views.manage_register, name='register_api'), 
    path('profileApi', views.profile, name='profileApi'),
    path("profile", views.profile_view, name="profile"),
    path('login', views.login_api, name='login'),
    path('check-session/', views.check_user_session, name='check_session'),
     path('get_uploaded_files/', views.get_uploaded_files, name='get_uploaded_files'),
    path('home/',views.homepage,name='home'),
    path('testresult',views.testresult,name="testresult"),
    path('schedule',views.schedule,name="schedule"),
    path('logout/', views.custom, name='logout'),
    path("update_medication_status/", update_medication_status, name="update_medication_status"),
    path("get_profile/", views.get_profiles, name="get_profile"),
    path("get_taken_status", views.get_taken_status, name="get_taken_status"),
    path("hello", views.hello, name="get_taken_status"),
  
    
    
    
    
    
]

    
   # if using class-based view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)