# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse ,JsonResponse
from matplotlib.dates import YEARLY
from .models import Faculty, Student, Subject, Attendance, FacultySubjectMapping
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required
from django.db.models import F ,Count, Value
from datetime import date, datetime
from django.contrib.auth.models import User
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from django.db.models.functions import Coalesce


def base(request):
    return render(request, 'base.html') 

def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        # Redirect to dashboard after login
            return redirect('admin_dashboard')  # Use the name defined in urlpatterns
        else:
            return render(request, 'admin/login.html', {'error': 'Invalid credentials'})
    return render(request, 'admin/login.html')


# Take Attendance (Faculty)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get('next', '/faculty/faculty_dashboard/'))
        else:
            return render(request, 'faculty/faculty_login.html', {'error': 'Invalid username or password'})
    return render(request, 'faculty/faculty_login.html')

@login_required
def faculty_dashboard(request):
    # This view will be accessible only to logged-in faculty
    return render(request, 'faculty/faculty_dashboard.html')  # Create a dashboard template for faculty

def faculty_logout(request):
    logout(request)
    return render(request, 'base.html')

# View Reports (Faculty)
def reports(request):
    return render(request, 'faculty/reports.html')


def subject_wise_reports(request):
    # Start the base query for subject-wise attendance report
    reports = Attendance.objects.values('subject__name') \
        .annotate(
            total_present=Count('id', filter=F('status') == Value("Present")),
            total_absent=Count('id', filter=F('status') == Value("Absent"))
        ).annotate(
            attendance_percentage=Coalesce(
                100.0 * F('total_present') / (F('total_present') + F('total_absent')),
                0.0
            )
        )
    # Handle file download if requested
    if 'download' in request.GET:
        file_type = request.GET.get('file_type')

        if file_type == 'excel':
            # Generate Excel file with filtered data
            df = pd.DataFrame(reports)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="subjectwise_report.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif file_type == 'pdf':
            # Generate PDF for subject-wise report
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="subjectwise_report.pdf"'

            # Create PDF using ReportLab
            pdf = canvas.Canvas(response, pagesize=letter)
            pdf.setFont("Helvetica", 10)

            # Add Title and Table Headers
            pdf.drawString(250, 750, "Subject-Wise Attendance Report")
            pdf.drawString(100, 730, "Subject")
            pdf.drawString(200, 730, "Attendance Percentage")

            # Add Table Rows
            y_position = 710
            for report in reports:
                pdf.drawString(100, y_position, str(report['subject__name']))
                pdf.drawString(200, y_position, f"{report['attendance_percentage']:.2f}%")
                y_position -= 20

            # Save PDF
            pdf.showPage()
            pdf.save()

            return response

    # Render the template with filtered reports
    return render(request, 'faculty/subject_wise_reports.html', {
        'reports': reports,
    })




def student_wise_reports(request):
    # Get filter parameters from the request
    year = request.GET.get('year')
    semester = request.GET.get('semester')

    # Base queryset: Annotate attendance percentages for each student
    reports = (
        Attendance.objects.values('student__name', 'student__year', 'student__semester')
        .annotate(
            total_present=Count('id', filter=F('status') == Value("Present")),
            total_absent=Count('id', filter=F('status') == Value("Absent")),
        )
        .annotate(
            attendance_percentage=Coalesce(
                100.0 * F('total_present') / (F('total_present') + F('total_absent')),
                0.0
            )
        )
    )
    # Apply filters if year and/or semester are provided
    if year:
        reports = reports.filter(student__year=year)
    if semester:
        reports = reports.filter(student__semester=semester)

    # Retrieve distinct years and semesters for the filter dropdowns
    years = Attendance.objects.values_list('student__year', flat=True).distinct()
    semesters = Attendance.objects.values_list('student__semester', flat=True).distinct()

    # Handle downloading if the user clicks on the download button
    if 'download' in request.GET:
        file_type = request.GET.get('file_type')

        if file_type == 'excel':
            # Generate Excel file with the filtered data
            df = pd.DataFrame(reports)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="student_wise_report.xlsx"'
            df.to_excel(response, index=False)
            return response
        elif file_type == 'pdf':
            # You can implement PDF generation logic here if needed
             # Generate PDF with filtered data
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="student_wise_report.pdf"'

            # Create PDF with ReportLab
            pdf = canvas.Canvas(response, pagesize=letter)
            pdf.setFont("Helvetica", 10)

            # Add Title
            pdf.drawString(250, 750, "Student-Wise Attendance Report")
            pdf.drawString(100, 730, f"Year: {year if year else 'All'}")
            pdf.drawString(100, 710, f"Semester: {semester if semester else 'All'}")

            # Add Table Header
            pdf.drawString(100, 690, "Student Name")
            pdf.drawString(300, 690, "Attendance Percentage")

            # Add Table Rows
            y_position = 670
            for report in reports:
                pdf.drawString(100, y_position, str(report['student__name']))
                pdf.drawString(300, y_position, f"{report['attendance_percentage']:.2f}%")
                y_position -= 20

            # Save the PDF
            pdf.showPage()
            pdf.save()

            return response

    # Render the template with context
    context = {
        'reports': reports,
        'years': years,
        'semesters': semesters,
        'year': year,
        'semester': semester,
    }
    return render(request, 'faculty/student_wise_reports.html', context)



def low_attendance_report(request):
    # Get filters for year and semester from the GET request
    year_filter = request.GET.get('year', None)
    semester_filter = request.GET.get('semester', None)

    # Base queryset for low attendance (students with attendance < 75%)
    reports = Attendance.objects.values('student__name', 'student__year', 'student__semester') \
        .annotate(
            total_present=Count('id', filter=F('status') == Value("Present")),
            total_absent=Count('id', filter=F('status') == Value("Absent"))
        ).annotate(
            attendance_percentage=Coalesce(
                100.0 * F('total_present') / (F('total_present') + F('total_absent')),
                0.0
            )
        ).filter(attendance_percentage__lt=75)

    # Apply year and semester filters if provided
    if year_filter:
        reports = reports.filter(student__year=year_filter)
    if semester_filter:
        reports = reports.filter(student__semester=semester_filter)

    # Handle downloading if the user clicks on the download button
    if 'download' in request.GET:
        file_type = request.GET.get('file_type')

        if file_type == 'excel':
            # Generate Excel file with the filtered data
            df = pd.DataFrame(reports)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="low_attendance_report.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif file_type == 'pdf':
            # Generate PDF for low attendance report
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="low_attendance_report.pdf"'

            # Create PDF with ReportLab
            pdf = canvas.Canvas(response, pagesize=letter)
            pdf.setFont("Helvetica", 10)

            # Add Title
            pdf.drawString(250, 750, "Low Attendance Report")
            pdf.drawString(100, 730, "Student Name")
            pdf.drawString(200, 730, "Year")
            pdf.drawString(300, 730, "Semester")
            pdf.drawString(400, 730, "Attendance Percentage")

            # Add Table Rows
            y_position = 710
            for report in reports:
                pdf.drawString(100, y_position, str(report['student__name']))
                pdf.drawString(200, y_position, str(report['student__year']))
                pdf.drawString(300, y_position, str(report['student__semester']))
                pdf.drawString(400, y_position, f"{report['attendance_percentage']:.2f}%")
                y_position -= 20

            # Save the PDF
            pdf.showPage()
            pdf.save()

            return response

    # Render the template with context
    return render(request, 'faculty/low_attendance_reports.html', {
        'reports': reports, 
        'year_filter': year_filter,
        'semester_filter': semester_filter,
    })




def daily_attendance_report(request):
    # Get filters for date, year, and semester from the GET request
    report_date = request.GET.get('date', str(date.today()))
    year_filter = request.GET.get('year', None)
    semester_filter = request.GET.get('semester', None)

    # Base queryset for daily attendance (filtering by date)
    reports = Attendance.objects.filter(date=report_date)

    # Apply year and semester filters if they are provided
    if year_filter:
        reports = reports.filter(student__year=year_filter)
    if semester_filter:
        reports = reports.filter(student__semester=semester_filter)

    # Annotate attendance percentage
    reports = (
        reports.values('student__name', 'student__year', 'student__semester')
        .annotate(
            total_present=Count('id', filter=F('status') == Value("Present")),
            total_absent=Count('id', filter=F('status') == Value("Absent")),
        )
        .annotate(
            attendance_percentage=Coalesce(
                100.0 * F('total_present') / (F('total_present') + F('total_absent')),
                0.0
            )
        )
    )

    # Handle downloading if the user clicks on the download button
    if 'download' in request.GET:
        file_type = request.GET.get('file_type')

        if file_type == 'excel':
            # Generate Excel file with the filtered data
            df = pd.DataFrame(reports)
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="daily_attendance_report.xlsx"'
            df.to_excel(response, index=False)
            return response

        elif file_type == 'pdf':
            # Generate PDF for daily attendance report
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="daily_attendance_report.pdf"'

            # Create PDF with ReportLab
            pdf = canvas.Canvas(response, pagesize=letter)
            pdf.setFont("Helvetica", 10)

            # Add Title
            pdf.drawString(250, 750, f"Daily Attendance Report for {report_date}")
            pdf.drawString(100, 730, "Student Name")
            pdf.drawString(200, 730, "Year")
            pdf.drawString(300, 730, "Semester")
            pdf.drawString(400, 730, "Attendance Percentage")

            # Add Table Rows
            y_position = 710
            for report in reports:
                pdf.drawString(100, y_position, str(report['student__name']))
                pdf.drawString(200, y_position, str(report['student__year']))
                pdf.drawString(300, y_position, str(report['student__semester']))
                pdf.drawString(400, y_position, f"{report['attendance_percentage']:.2f}%")
                y_position -= 20

            # Save the PDF
            pdf.showPage()
            pdf.save()

            return response

    # Render the template with context
    return render(request, 'faculty/daily_report.html', {
        'reports': reports, 
        'date': report_date,
        'year_filter': year_filter,
        'semester_filter': semester_filter,
    })



@login_required
def take_attendance(request):
    user = request.user  # Logged-in faculty user

    try:
        faculty = Faculty.objects.get(user=user)  # Validate faculty instance
    except Faculty.DoesNotExist:
        return render(request, 'faculty/take_attendance.html', {
            'error': 'You are not assigned as a faculty. Please contact the administrator.',
        })

    today_date = date.today().strftime('%Y-%m-%d')  # Get today's date
    subjects = FacultySubjectMapping.objects.filter(faculty=faculty).select_related('subject')  # Fetch all subjects assigned to faculty

    if request.method == 'POST':
        # Fetch form data
        subject_id = request.POST.get('subject')
        period = request.POST.get('period')  # Retrieve period from POST request

        # Validate inputs
        if not subject_id:
            return render(request, 'faculty/take_attendance.html', {
                'error': 'Please select a subject.',
                'today_date': today_date,
                'subjects': subjects,
            })

        if not period:
            return render(request, 'faculty/take_attendance.html', {
                'error': 'Period is required.',
                'today_date': today_date,
                'subjects': subjects,
            })

        try:
            # Get the selected subject and its details
            selected_subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return render(request, 'faculty/take_attendance.html', {
                'error': 'The selected subject does not exist.',
                'today_date': today_date,
                'subjects': subjects,
            })

        # Redirect to mark attendance with necessary parameters
        return redirect('mark_attendance', 
                        year=selected_subject.year, 
                        semester=selected_subject.semester, 
                        subject_code=selected_subject.subject_code, 
                        period=period)

    # Render initial form
    return render(request, 'faculty/take_attendance.html', {
        'subjects': [mapping.subject for mapping in subjects],  # List of subjects for dropdown
        'today_date': today_date,
    })


@login_required
def mark_attendance(request, year, semester, subject_code, period):
    try:
        # Fetch students and subject based on year, semester, and subject_code
        students = Student.objects.filter(year=year, semester=semester)
        subject = Subject.objects.get(subject_code=subject_code)
    except Subject.DoesNotExist:
        # Handle the case where the subject doesn't exist
        return redirect('take_attendance')  # Redirect back to take_attendance if subject is not found

    if request.method == 'POST':
        date_input = request.POST.get('date', str(date.today()))  # Use .get() to handle missing keys
        
        for student in Student.objects.filter(year=year, semester=semester):
            student_id = student.student_id
            # Check if the checkbox is checked (Present)
            status = 'Present' if f'status_{student_id}' in request.POST else 'Absent'
           
            # Process attendance data for all students (optional, based on your use case)
            attendance_data = []
        
            attendance_data.append(Attendance(
                student=student,
                subject=subject,
                date=date.today(),
                status=status,
                period=period  # Include the period in the attendance record
            ))

        # Bulk create attendance records (optional, only if necessary)
        Attendance.objects.bulk_create(attendance_data)

        # After successfully saving the attendance, redirect to the save_attendance page
        return redirect('save_attendance', year=year, semester=semester, subject_code=subject_code, period=period)

    # Render the 'mark_attendance' page with the required context for GET requests
    return render(request, 'faculty/mark_attendance.html', {
        'students': students,
        'subject': subject,
        'year': year,
        'semester': semester,
        'period': period,
        'date': date.today().strftime('%Y-%m-%d'),
    })


@login_required
def save_attendance(request, year, semester, subject_code,period):
    try:
        # Fetch the subject based on the subject_code
        subject = Subject.objects.get(subject_code=subject_code)
        
        # Fetch students based on year and semester
        students = Student.objects.filter(year=year, semester=semester)

        # Check if attendance data is available for this subject, year, and semester
        attendance_records = Attendance.objects.filter(
            subject=subject,
            date=date.today(),
        )

        # If no attendance records are found, redirect back to mark attendance
        if not attendance_records:
            return redirect('take_attendance')

    except Subject.DoesNotExist:
        # If the subject does not exist, redirect to take attendance
        return redirect('take_attendance')

    # Render the save_attendance page with success message
    return render(request, 'faculty/save_attendance.html', {
        'year': year,
        'semester': semester,
        'subject': subject,
        'period':period,
        'attendance_records': attendance_records,
        'date': date.today().strftime('%Y-%m-%d'),
        
    })


