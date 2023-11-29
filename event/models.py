from django.db import models
from django.contrib.auth.models import User



    

class EventType(models.Model):
    STATE_CHOICES=[
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam','Assam'),
        ('Bihar','Bihar'),
        ('Chhattisgarh','Chhattisgarh'),
        ('Goa','Goa'),
        ('Gujarat','Gujarat'),
        ('Haryana','Haryana'),
        ('Himachal Pradesh','Himachal Pradesh'),
        ('Jharkhand','Jharkhand'),
        ('Karnataka','Karnataka'),
        ('Kerala','Kerala'),
        ('Madhya Pradesh','Madhya Pradesh'),
        ('Maharashtra','Maharashtra'),
        ('Manipur','Manipur'),
        ('Meghalaya','Meghalaya'),
        ('Mizoram','Mizoram'),
        ('Nagaland','Nagaland'),
        ('Odisha','Odisha'),
        ('Punjab','Punjab'),
        ('Rajasthan','Rajasthan'),
        ('Sikkim','Sikkim'),
        ('Tamil Nadu','Tamil Nadu'),
        ('Telangana','Telangana'),
        ('Tripura','Tripura'),
        ('Uttar Pradesh','Uttar Pradesh'),
        ('Uttarakhand','Uttarakhand'),
        ('West Bengal','West Bengal'),
    ]
    ename = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    venue = models.CharField(max_length=100, choices=STATE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.ename