# Generated by Django 3.2 on 2023-11-03 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0011_auto_20231027_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='customer_confidence',
            field=models.CharField(choices=[('certain', 'Certain'), ('uncertain', 'Uncertain'), ('confident', 'Confident')], max_length=20, null=True),
        ),
    ]
