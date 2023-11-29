# Generated by Django 4.2.4 on 2023-10-08 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_alter_contact_engaged_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contactproduct',
            name='product_name',
        ),
        migrations.AddField(
            model_name='contactproduct',
            name='product',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='app1.producttype'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='contact',
            name='interested_products',
        ),
        migrations.AddField(
            model_name='contact',
            name='interested_products',
            field=models.ManyToManyField(through='app1.ContactProduct', to='app1.producttype'),
        ),
    ]