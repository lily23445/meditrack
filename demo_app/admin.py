from django.contrib import admin
from .models import register,UploadedFile,MedicineLog,MedicineStatus,Profile
# Register your models here.
admin.site.register(register)
admin.site.register(UploadedFile)
admin.site.register(MedicineLog)
admin.site.register(MedicineStatus)
admin.site.register(Profile)



