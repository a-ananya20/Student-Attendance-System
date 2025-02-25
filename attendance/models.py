from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Faculty model
class Faculty(models.Model):
    faculty_id = models.CharField(max_length=10, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    def __str__(self):
        return f"{self.name} ({self.faculty_id})"


# Student model
class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    def __str__(self):
        return f"{self.name} ({self.student_id})"


# Subject model
class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    semester = models.IntegerField()
    def __str__(self):
        return f"{self.name} ({self.subject_code})"


# Attendance model
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    period = models.IntegerField() 
    status = models.CharField(max_length=10) # True for Present, False for Absent
    class Meta:
        unique_together = ('student', 'subject', 'date', 'period')
    def __str__(self):
        return f"Attendance for {self.student.name} in {self.subject.name} on {self.date}"


class FacultySubjectMapping(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = ('faculty', 'subject')  # Prevent duplicate mappings
    def __str__(self):
        return f"{self.faculty.name} -> {self.subject.name}"
