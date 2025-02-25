# Register your models here.
from django.contrib import admin
from .models import Faculty, Student, Subject, Attendance, FacultySubjectMapping
from django.db import connection  # For raw SQL queries
from django.contrib import messages

# Register Faculty and Subject models directly
admin.site.register(Faculty)
admin.site.register(Subject)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'period', 'status')
    list_filter = ('subject', 'date')
    search_fields = ('student__name', 'subject__name')


@admin.register(FacultySubjectMapping)
class FacultySubjectMappingAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'subject', 'assigned_date')
    search_fields = ('faculty__name', 'subject__name')
    list_filter = ('faculty', 'subject')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('faculty', 'subject')

    actions = ['map_faculty_to_subject']

    def map_faculty_to_subject(self, request, queryset):
        # This action allows manual mapping from the admin interface
        for mapping in queryset:
            pass
        self.message_user(request, f"Faculty to Subject mapping updated for {queryset.count()} records.")

    map_faculty_to_subject.short_description = "Map selected faculty to subjects"



class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'year', 'semester')
    list_filter = ('year', 'semester')
    search_fields = ('name', 'student_id')
    actions = ['import_students_from_table']

    
# Register the Student model with the custom admin class
admin.site.register(Student, StudentAdmin)
