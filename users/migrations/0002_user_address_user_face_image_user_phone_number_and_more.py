# Generated by Django 4.2.16 on 2024-11-15 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='face_image',
            field=models.ImageField(blank=True, null=True, upload_to='face_images/'),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='voice_sample',
            field=models.FileField(blank=True, null=True, upload_to='voice_samples/'),
        ),
    ]
