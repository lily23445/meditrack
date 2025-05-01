# Create your models here.
from datetime import date, timedelta
from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now # type: ignore




class register(AbstractUser):
   
    username=models.CharField(max_length=50)
    email=models.EmailField(unique=True,primary_key=True)
    password=models.CharField(max_length=250)
    
    
    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username'] 
  
    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password when creating a new user
            self.set_password(self.password)  # Hash the password
        super().save(*args, **kwargs)

    
    def set_password(self, password):
        self.password = make_password(password)

    # This method checks the password using the hashed value
    def check_password(self, password):
        return check_password(password, self.password)
    


class Profile(models.Model):
    user = models.OneToOneField(register, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=[("Male", "Male"), ("Female", "Female")])
    blood_group = models.CharField(
        max_length=3, 
        choices=[("A+", "A+"), ("B+", "B+"), ("AB+", "AB+"), ("O+", "O+"), 
                 ("A-", "A-"), ("B-", "B-"), ("AB-", "AB-"), ("O-", "O-")]
    )

    def __str__(self):
        return f"{self.user.email} - {self.full_name}"

class UploadedFile(models.Model):
    user = models.ForeignKey(register, on_delete=models.CASCADE, to_field="email")  
    file = models.FileField(upload_to="user_uploads/",null=True,blank=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.file.name}"
    

class MedicineLog(models.Model):
    print("It came here to find get")
    user = models.ForeignKey(register, on_delete=models.CASCADE, to_field="email")  
    medicine_name = models.CharField(max_length=255)
    start_date = models.DateField(default=date.today)  # New field
    end_date = models.DateField(default=date.today)    # New field
    time = models.CharField(
        max_length=50,
        choices=[("morning", "Morning"), ("afternoon", "Afternoon"), ("night", "Night")],
    )  

     # Stores status as a dictionary for each date
    

  

    def get_date_range(self):
        return [self.start_date + timedelta(days=i) for i in range((self.end_date - self.start_date).days + 1)]
  
    def __str__(self):
        return f"{self.user.email} - {self.medicine_name}"

from django.db import models
from datetime import date

class MedicineStatus(models.Model):
    medicine_log = models.ForeignKey(MedicineLog, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=[('taken', 'Taken'), ('missed', 'Missed')], default='missed')
    def __str__(self):
        return f"{self.medicine_log.medicine_name} on {self.date} - {self.status} {self.medicine_log.time}"
