# from django_cron import CronJobBase, Schedule
# from django.core.mail import send_mail
# from your_app.models import register  # Use your actual user model

# class SendEmailCronJob(CronJobBase):
#     schedule = Schedule(run_at_times=['09:00', '13:00', '17:00'])  # 9 AM, 1 PM, 5 PM
#     code = 'your_app.send_email_cron'  # Unique code

#     def do(self):
#         users = register.objects.all()
#         for user in users:
#             send_mail(
#                 'Scheduled Email',
#                 'This is your scheduled email!',
#                 'from@example.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#         print("Emails sent successfully!")

from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail

class SendEmailCronJob(CronJobBase):
    schedule = Schedule(run_every_mins=1)  # Runs every 1 minute for testing
    code = 'your_app.send_email_cron'  # Unique identifier

    def do(self):
        send_mail(
            'Test Email from Cron',
            'This is a test email sent by django-cron.',
            'demoapp2345@gmail.com',  # Replace with sender email
            ['p.kalash017@example.com'],  # Replace with recipient email
            fail_silently=False,
        )
        print("Email sent successfully!")
