# Generated by Django 5.0.2 on 2024-04-02 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_room_admin_alter_room_members'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]