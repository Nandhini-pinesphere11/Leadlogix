# Generated by Django 3.2 on 2023-11-02 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_country_code', models.CharField(choices=[('+91', '+91'), ('+93', '+93'), ('+54', '+54'), ('+61', '+61'), ('+43', '+43'), ('+32', '+32'), ('+55', '+55'), ('+86', '+86'), ('+53', '+53'), ('+45', '+45'), ('+20', '+20'), ('+33', '+33'), ('+49', '+49'), ('+30', '+30'), ('+36', '+36'), ('+62', '+62'), ('+98', '+98'), ('+39', '+39'), ('+81', '+81'), ('+82', '+82'), ('+60', '+60'), ('+52', '+52'), ('+95', '+95'), ('+31', '+31'), ('+64', '+64'), ('+47', '+47'), ('+92', '+92'), ('+51', '+51'), ('+63', '+63'), ('+48', '+48'), ('+40', '+40'), ('+65', '+65'), ('+27', '+27'), ('+34', '+34'), ('+94', '+94'), ('+46', '+46'), ('+41', '+41'), ('+66', '+66'), ('+44', '+44'), ('+90', '+90'), ('+58', '+58'), ('+84', '+84'), ('+967', '+967'), ('+263', '+263'), ('+260', '+260'), ('+678', '+678'), ('+688', '+688'), ('+993', '+993'), ('+677', '+677'), ('+221', '+221'), ('+379', '+379'), ('+256', '+256'), ('+380', '+380'), ('+971', '+971'), ('+998', '+998'), ('+216', '+216'), ('+249', '+249'), ('+677', '+677'), ('+252', '+252'), ('+966', '+966'), ('+381', '+381'), ('+974', '+974'), ('+351', '+351'), ('+968', '+968'), ('+680', '+680'), ('+507', '+507'), ('+234', '+234'), ('+977', '+977'), ('+377', '+377'), ('+976', '+976'), ('+212', '+212'), ('+258', '+258'), ('+965', '+965'), ('+230', '+230'), ('+856', '+856'), ('+961', '+961'), ('+231', '+231'), ('+218', '+218'), ('+370', '+370'), ('+352', '+352'), ('+261', '+261'), ('+960', '+960'), ('+962', '+962'), ('+254', '+254'), ('+850', '+850'), ('+964', '+964'), ('+353', '+353'), ('+972', '+972'), ('+299', '+299'), ('+852', '+852'), ('+354', '+354'), ('+251', '+251'), ('+679', '+679'), ('+358', '+358'), ('+242', '+242'), ('+855', '+855'), ('+975', '+975'), ('+880', '+880'), ('+1', '+1'), ('+7', '+7')], max_length=5, null=True)),
                ('phone_number', models.CharField(max_length=15)),
                ('reference_number', models.CharField(max_length=50)),
                ('contact_person', models.CharField(max_length=100)),
                ('plan_name', models.CharField(max_length=100)),
                ('subscription_details', models.TextField()),
                ('address1', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh', 'Arunachal Pradesh'), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal')], max_length=100)),
                ('address2', models.CharField(max_length=100)),
                ('postcode', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=50)),
            ],
        ),
    ]
