from django.core.management.base import BaseCommand
from datetime import date, timedelta
from django.core.mail import send_mail
from profileaddition.models import Profile
import time
from django.db import models

class Command(BaseCommand):
    help = 'Send renewal alerts for profiles'

    def handle(self, *args, **options):
        print("Renewal alerts checking started...")

        # Define the number of days before renewal to send alerts
        alert_timedelta = timedelta(days=7)  # You can change this as needed

        continuous_execution = True

        while continuous_execution:
            # Calculate the date range for sending alerts
            today = date.today()
            one_week_before = today + alert_timedelta
            one_month_before = today + timedelta(days=30)
            one_day_before = today + timedelta(days=1)

                        # Profiles that are due for renewal in one week or have changed dates
            profiles_one_week = Profile.objects.filter(
                (models.Q(end_date__lte=one_week_before, end_date__gte=today) |
                models.Q(from_date__lte=one_week_before, from_date__gte=today))
            )

            # Profiles that are due for renewal in one month or have changed dates
            profiles_one_month = Profile.objects.filter(
                (models.Q(end_date__lte=one_month_before, end_date__gte=today) |
                models.Q(from_date__lte=one_month_before, from_date__gte=today))
            )

            # Profiles that are due for renewal one day before or have changed dates
            profiles_one_day = Profile.objects.filter(
                (models.Q(end_date__lte=one_day_before, end_date__gte=today) |
                models.Q(from_date__lte=one_day_before, from_date__gte=today))
            )

            # Profiles that are due for renewal on the same day or have changed dates
            profiles_today = Profile.objects.filter(
                (models.Q(end_date=today) | models.Q(from_date=today))
            )

            # Print renewal process start message
            print("Renewal process started...")

            # Loop through the profiles and send renewal alerts
            for profile in profiles_one_week:
                self.send_alert(profile, 'One week left for renewal')

            for profile in profiles_one_month:
                self.send_alert(profile, 'One month left for renewal')

            for profile in profiles_one_day:
                self.send_alert(profile, 'One day left for renewal')

            for profile in profiles_today:
                self.send_alert(profile, 'Renewal is due today')

            # Print renewal process complete message
            print("Renewal process complete. Waiting for the next check...")

            # Add a delay of 24 hours before checking again
            time.sleep(24 * 60 * 60)


            # Set continuous_execution to False to stop the loop (you can add a condition to stop based on your requirement)
            continuous_execution = False

    def send_alert(self, profile, message):
        # Customize the email subject and body as needed
        subject = 'Renewal Alert'
        body = f"Hello {profile.user.username},\n\n{message} for your profile. Please renew your subscription as soon as possible."

        # Send the alert email
        send_mail(subject, body, 'leadlogix.communications@gmail.com', [profile.email])
        print(f"Renewal alert sent to {profile.user.username} ({profile.email})")
