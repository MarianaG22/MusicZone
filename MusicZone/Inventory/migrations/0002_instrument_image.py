# Generated by Django 5.1.6 on 2025-05-02 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='image',
            field=models.ImageField(default=None, upload_to='galery/'),
        ),
    ]
