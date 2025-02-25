# Generated by Django 4.2.16 on 2024-12-02 13:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def forwards(apps, schema_editor):
    Faculty = apps.get_model('attendance', 'Faculty')
    User = apps.get_model('auth', 'User')
    # Create a default user for existing faculty if needed (if user is required)
    for faculty in Faculty.objects.all():
        # Assign a user to the faculty if necessary
        user = User.objects.create(username=faculty.name)  # Example logic
        faculty.user = user
        faculty.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attendance', '0002_alter_subject_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
