# Generated by Django 3.1.14 on 2023-12-08 11:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='vendorprofile',
            name='vendor_code',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
