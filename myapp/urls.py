from django.urls import path
from . import views
from .views import create_teacher, create_student
urlpatterns = [
    path('login/', views.login_view, name='login'),
    
    # Admin Views
    path('ads/<int:user_id>/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('send_message_to_teacher/', views.send_message_to_teacher, name='send_message_to_teacher'),
    path('create-teacher/', create_teacher, name='create_teacher'),
    path('create-student/', create_student, name='create_student'),
    path('create_class/', views.create_class, name='create_class'),
    #path('student/update/<int:student_id>/', views.student_update, name='student_update'),
    #path('teacher/update/<int:teacher_id>/', views.teacher_update, name='teacher_update'),
    path('ads/student/update/<int:student_id>/', views.admin_update_student, name='ads_student_update'),
    path('ads/teacher/update/<int:teacher_id>/', views.admin_update_teacher, name='ads_teacher_update'),
    path('ads/class/update/<str:class_name>/', views.admin_update_class ,name='ads_class_update'),
    path('ads/student/delete/<int:student_id>/', views.delete_student, name='delete_student'),
    path('ads/teacher/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('ads/class/delete/<str:class_name>/', views.delete_class ,name='delete_class'),
    path('students/', views.student_list, name='student_list'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    #path('ads/messages/<int:admin_id>/', views.get_sended_messages, name='ads_messages'),
    
    # Teacher Views
    path('teacher/<int:user_id>/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('generate_teacher_report/<int:teacher_id>/', views.generate_teacher_report, name='generate_teacher_report'),
    path('send_message_to_student/', views.send_message_to_student, name='send_message_to_student'),
    
    # Student Views
    path('student/<int:student_id>/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('generate_report/<int:student_id>/', views.generate_report, name='generate_report'),
    path('predict/<int:student_id>/', views.predict_student_result, name='predict_student_result'),
    
]
