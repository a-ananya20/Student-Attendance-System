from django.urls import path 
from . import views


urlpatterns = [

    # home URL 
    path('', views.base, name='base'),
    path('admin/login/', views.custom_login, name='login'),

    # Faculty URLs
    path('faculty/faculty_login/',views.login_view , name='login_view'),
    path('faculty/faculty_dashboard/',views.faculty_dashboard,name='faculty_dashboard'),
    path('faculty/logout/', views.faculty_logout, name='faculty_logout'),
    path('faculty/take_attendance/', views.take_attendance, name='take_attendance'),
    path('faculty/mark_attendance/<str:year>/<str:semester>/<str:subject_code>/<str:period>/', views.mark_attendance , name ='mark_attendance'),
    path('faculty/save_attendance/<int:year>/<int:semester>/<str:subject_code>/<str:period>/', views.save_attendance, name='save_attendance'),
    path('faculty/dashboard/reports/', views.reports, name='reports'),
    path('faculty/dashboard/reports/daily/', views.daily_attendance_report, name='daily_report'),
    path('faculty/dashboard/reports/subject-wise/', views.subject_wise_reports, name='subject_wise_reports'),
    path('faculty/dashboard/reports/student-wise/', views.student_wise_reports, name='student_wise_reports'),
    path('faculty/dashboard/reports/low-attendance/', views.low_attendance_report, name='low_attendance_reports'),
    # path('download_report/', views.download_report, name='download_report'),  
]
