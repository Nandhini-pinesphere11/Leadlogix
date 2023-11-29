from django.db import models
from django.contrib.auth.models import User

STATE_CHOICES = [
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

COUNTRY_CODE_CHOICES = [
        ('+91', '+91'),
        ('+93', '+93'),
        ('+54','+54'),
        ('+61','+61'),
        ('+43','+43'),
        ('+32','+32'),
        ('+55','+55'),
        ('+86','+86'),
        ('+53','+53'),
        ('+45','+45'),
        ('+20','+20'),
        ('+33','+33'),
        ('+49','+49'),
        ('+30','+30'),
        ('+36','+36'),
        ('+62','+62'),
        ('+98','+98'),
        ('+39','+39'),
        ('+81','+81'),
        ('+82','+82'),
        ('+60','+60'),
        ('+52','+52'),
        ('+95','+95'),
        ('+31','+31'),
        ('+64','+64'),
        ('+47','+47'),
        ('+92','+92'),
        ('+51','+51'),
        ('+63','+63'),
        ('+48','+48'),
        ('+40','+40'),
        ('+65','+65'),
        ('+27','+27'),
        ('+34','+34'),
        ('+94','+94'),
        ('+46','+46'),
        ('+41','+41'),
        ('+66','+66'),
        ('+44','+44'),
        ('+90','+90'),
        ('+58','+58'),
        ('+84','+84'),
        ('+967','+967'),
        ('+263','+263'),
        ('+260','+260'),
        ('+678','+678'),
        ('+688','+688'),
        ('+993','+993'),
        ('+677','+677'),
        ('+221','+221'),
        ('+379','+379'),
        ('+256','+256'),
        ('+380','+380'),
        ('+971','+971'),
        ('+998','+998'),
        ('+216','+216'),
        ('+249','+249'),
        ('+677','+677'),
        ('+252','+252'),
        ('+966','+966'),
        ('+381','+381'),
        ('+974','+974'),
        ('+351','+351'),
        ('+968','+968'),
        ('+680','+680'),
        ('+507','+507'),
        ('+234','+234'),
        ('+977','+977'),
        ('+377','+377'),
        ('+976','+976'),
        ('+212','+212'),
        ('+258','+258'),
        ('+965','+965'),
        ('+230','+230'),
        ('+856','+856'),
        ('+961','+961'),
        ('+231','+231'),
        ('+218','+218'),
        ('+370','+370'),
        ('+352','+352'),
        ('+261','+261'),
        ('+960','+960'),
        ('+962','+962'),
        ('+254','+254'),
        ('+850','+850'),
        ('+964','+964'),
        ('+353','+353'),
        ('+972','+972'),
        ('+299','+299'),
        ('+852','+852'),
        ('+354','+354'),
        ('+251','+251'),
        ('+679','+679'),
        ('+358','+358'),
        ('+242','+242'),
        ('+855','+855'),
        ('+975','+975'),
        ('+880','+880'),
        ('+1','+1'),
        ('+7','+7'),
]

# Create your models here.
class Vendor(models.Model):
     
    first_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    country_code = models.CharField(max_length=10, choices=COUNTRY_CODE_CHOICES)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    product_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    website_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    same_industry = models.BooleanField(default=False)
    specific_appointment = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
    
class DepartmentType(models.Model):
    dname = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # Add a default value
    emailaddress = models.EmailField()

    def __str__(self):
        return self.dname
    
    
