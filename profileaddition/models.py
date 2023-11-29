from django.db import models
from django.contrib.auth.models import Group, User

class GroupSpecificUserManager(models.Manager):
    def get_queryset(self):
        # Replace 'Strings' with the name of the group you want to filter by
        group_name = 'Strings'
        group = Group.objects.get(name=group_name)
        users_in_group = group.user_set.all()
        return super().get_queryset().filter(user__in=users_in_group)
    
class Profile(models.Model):
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
    COUNTRY_CODE_CHOICES=[
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

    PLAN_CHOICES = [
        ('1 Month', '1 Month'),
        ('6 Months', '6 Months'),
        ('1 Year', '1 Year'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'is_active': True},
        related_name='profile',
        verbose_name='User',
    )
    objects = GroupSpecificUserManager()

    company_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_country_code = models.CharField(max_length=5, choices=COUNTRY_CODE_CHOICES,null=True)
    phone_number = models.CharField(max_length=15)
    reference_number = models.CharField(max_length=50)
    contact_person = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    address2 = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    plan_name = models.CharField(max_length=100, choices=PLAN_CHOICES)

    from_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Set the changed flags when dates are updated
        if self.pk:
            original_profile = Profile.objects.get(pk=self.pk)
            if self.from_date != original_profile.from_date:
                self.from_date_changed = True
            if self.end_date != original_profile.end_date:
                self.end_date_changed = True
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.company_name
