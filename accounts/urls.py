from . import views_subjects
from . import views_disciplines
from . import views_reports
from . import views_student_groups
from . import views_class
from . import views_attendances

from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,  TokenVerifyView)
#from rest_framework import routers


""" router = routers.DefaultRouter()
router.register(r'subjects',views_simple.SubjectsView, 'subject')
router.register(r'students',views_simple.StudentsView, 'student')
router.register(r'users',views_simple.UserView, 'user')
router.register(r'attendance',views_simple.AttendanceView, 'attendance')
router.register(r'horario',views_simple.HorarioView, 'horario') """


urlpatterns = [  
    #Disciplines
    path('disciplines/', views_disciplines.Disciplines_allView.as_view({'get': 'list_disciplines', 'post': 'create_discipline'}), name='disciplines-list'),
    path('disciplines/<int:discipline_pk>/', views_disciplines.Disciplines_allView.as_view({'get': 'retrieve_discipline', 'put': 'update_discipline', 'delete': 'delete_discipline'}), name='subject-detail'),
    #Subjects
    path('disciplines/<int:discipline_pk>/subjects/', views_subjects.Subjects_allView.as_view({'get': 'list_subjects', 'post': 'create_subject'}), name='subjects-list'),
    path('subjects/<int:subject_pk>/', views_subjects.Subjects_allView.as_view({'get': 'retrieve_subject', 'patch': 'update_subject', 'delete': 'delete_subject'}), name='subject-detail'),
    path('subjects/<int:subject_pk>/students/', views_subjects.SubjectsStudents.as_view({'get': 'get_students', 'post': 'post_student', 'delete': 'delete_student'}), name='subject-add-alumno'),
    path('subjects/<int:subject_pk>/students-auto/', views_subjects.SubjectsStudentAuto.as_view({'post': 'post_student_auto', 'delete': 'delete_student_auto'}), name='subject-add-alumno-auto'),
    path('subjects/<int:subject_pk>/teacher-go-off/', views_subjects.SubjectsExitTeacher.as_view({'delete': 'exit_teacher_auto'}), name='teacher-go-off-auto'),
    #Groups    
    path('subjects/<int:subject_pk>/groups/', views_student_groups.StudentGroups_allView.as_view({'get': 'list_groups', 'post': 'create_group'}), name='group-list'),
    path('groups/<int:group_pk>/', views_student_groups.StudentGroups_allView.as_view({'get': 'retrieve_group', 'put': 'update_group', 'delete': 'delete_group'}), name='group-detail'),
    #Ultimo cambio se saca subjects para ver el id de un horario, al parecer despues hay que hacer lo mismo con las otras urls
    path('groups/<int:group_pk>/students/', views_student_groups.ManageStudentOfGroup.as_view({'get': 'get_students_of_group', 'post': 'post_student_to_group', 'delete': 'delete_student_of_group'}), name='manage-student-group'),
    #Este delete pide "alumno_pk"
    #ACA se elimina porque los grupos ahora pasan solo a ser de utilidad a los profesores
    #path('grupos/<int:grupo_pk>/alumnos-auto/', views_grupos.HorarioAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),

    
    
    #Class
    path('subjects/<int:subject_pk>/class/<str:date>/', views_class.Subjects_Class_allView.as_view({'get': 'list'}), name='subject-allClass-of-day'),
    path('subjects/<int:subject_pk>/class/', views_class.ClassInstance_allView.as_view({'get': 'list_class', 'post': 'create_class'}), name='clase-list'),
    path('class/<int:class_pk>/', views_class.ClassInstance_allView.as_view({'get': 'retrieve_class', 'put': 'update_class', 'delete': 'delete_class'}), name='clase-detail'),
    #Attendance
    path('class/<int:class_pk>/attendances/', views_attendances.Attendances_allView.as_view({'get': 'list_attendances', 'post': 'create_attendancecreate_attendance'}), name='asistencia-list'),
    path('attendances/<int:attendance_pk>/', views_attendances.Attendances_allView.as_view({'get': 'retrieve_attendance', 'put': 'update_attendance', 'delete': 'delete_attendance'}), name='asistencia-detail'),
    #Hacer URL que devuelva la cantidad de asistencias e inasistencias de un alumno
    #path('asistencias/<int:alumno_pk>/'),
    path('class/<int:class_pk>/attendances/create-default/', views_attendances.AttendanceOfClass.as_view({'post': 'create_default'}), name='asistencia-create-default'),
    #El de arriba esta bien crea todas las asistencias de los alumnos del horario pero el horario lo consigue la funcion
    #path('courses/<int:course_pk>/subjectss2/', views_subjects_2.Subjects_allView.as_view({'get': 'list'}), name='subjects-list2'),
    #path('all-subjects/', SubjectsView.as_view({'get': 'all_subjects'}), name='all-subjects'),
    #Report
    path('info/subjects/<int:subject_pk>/',views_reports.subject_attendance_info, name='subject-attendance-info'),
   
]