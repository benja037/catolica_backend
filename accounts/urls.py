from . import views_subjects
from . import views_disciplines
from . import views_reports
from . import views_student_groups
from . import views_class
from . import views_attendances
from . import views_students
from . import views_requests

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
    #Students
    path('students/', views_students.Students_allView.as_view({'get': 'list_students', 'post': 'create_student'}), name='students-list'),
    path('students/<int:student_pk>/', views_students.Students_allView.as_view({'get': 'retrieve_student', 'put': 'update_student'}), name='student-detail'),
    path('students/check-rut/<str:tipo_documento>/<str:numero_documento>/', views_students.Students_check_rutView.as_view({'get': 'check_rut'}), name='check-rut-student'),
    #Students of user "apoderado"
    path('students/get-user-students/', views_students.Students_of_userView.as_view({'get': 'list_students_of_user'}), name='get-students-of-user'),
    path('students/post-user-students/', views_students.Students_of_userView.as_view({'post': 'create_student_of_user'}), name='post-students-of-user'),

     
    #Disciplines
    path('disciplines/', views_disciplines.Disciplines_allView.as_view({'get': 'list_disciplines', 'post': 'create_discipline'}), name='disciplines-list'),
    path('disciplines/<int:discipline_pk>/', views_disciplines.Disciplines_allView.as_view({'get': 'retrieve_discipline', 'put': 'update_discipline', 'delete': 'delete_discipline'}), name='subject-detail'),
    #Subjects
    path('disciplines/<int:discipline_pk>/subjects/', views_subjects.Subjects_Get_Post.as_view({'get': 'list_subjects', 'post': 'create_subject'}), name='subjects-list'),
    path('subjects/<int:subject_pk>/', views_subjects.Subjects_Retrieve_Delete_Patch.as_view({'get': 'retrieve_subject', 'patch': 'update_subject', 'delete': 'delete_subject'}), name='subject-detail'),
    path('subjects/<int:subject_pk>/students/', views_subjects.SubjectsStudents.as_view({'get': 'get_students', 'post': 'post_student'}), name='subject-add-alumno'),
    path('subjects/<int:subject_pk>/students/<int:student_pk>/', views_subjects.SubjectsStudents.as_view({'delete': 'delete_student'}), name='subject-remove-alumno'),
    path('subjects/<int:subject_pk>/no-students/', views_subjects.SubjectsStudents.as_view({'get': 'get_no_students'}), name='subject-no-student'),    
    path('subjects/<int:subject_pk>/teacher-go-off/', views_subjects.SubjectsExitTeacher.as_view({'delete': 'exit_teacher_auto'}), name='teacher-go-off-auto'),
    #Subjects apoderados
    path('apoderados/disciplines/<int:discipline_pk>/subjects/', views_subjects.Apoderados_Subjects_Get.as_view({'get': 'list_subjects'}), name='apoderados-subject'),
    path('apoderados/subjects/<int:subject_pk>/', views_subjects.Apoderados_Subjects_Retrieve.as_view({'get': 'retrieve_subject'}), name='apoderados-subject-detail'),
    path('apoderados/subjects/<int:subject_pk>/students-auto-add/', views_subjects.Apoderados_Subject_Post_add.as_view({'post': 'post_student_auto'}), name='subject-add-alumno-auto'),
    path('apoderados/subjects/<int:subject_pk>/students-auto-remove/', views_subjects.Apoderados_Subject_delete.as_view({'delete': 'delete_student_auto'}), name='subject-remove-alumno-auto'),
    #Groups    
    path('subjects/<int:subject_pk>/groups/', views_student_groups.StudentGroups_allView.as_view({'get': 'list_groups', 'post': 'create_group'}), name='group-list'),
    path('subjects/<int:subject_pk>/groups/<int:group_pk>/', views_student_groups.StudentGroups_allView.as_view({'get': 'retrieve_group', 'put': 'update_group', 'delete': 'delete_group'}), name='group-detail'),
    #Ultimo cambio se saca subjects para ver el id de un horario, al parecer despues hay que hacer lo mismo con las otras urls
    path('subjects/<int:subject_pk>/groups/<int:group_pk>/students/', views_student_groups.ManageStudentOfGroup.as_view({'get': 'get_students_of_group', 'post': 'post_student_to_group', 'delete': 'delete_student_of_group'}), name='manage-student-group'),
    path('subjects/<int:subject_pk>/groups/<int:group_pk>/no-students/', views_student_groups.ManageStudentOfGroup.as_view({'get': 'get_no_students_of_group'}), name='get-no-student-group'),
    #Este delete pide "alumno_pk"
    #ACA se elimina porque los grupos ahora pasan solo a ser de utilidad a los profesores
    #path('grupos/<int:grupo_pk>/alumnos-auto/', views_grupos.HorarioAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),

    
    
    #Class Teacher
    path('subjects/<int:subject_pk>/class-date/<str:date>/', views_class.Subjects_Class_allView.as_view({'get': 'list'}), name='subject-allClass-of-day'),
    path('subjects/<int:subject_pk>/class/', views_class.ClassInstance_allView.as_view({'get': 'list_class', 'post': 'create_class'}), name='clase-list'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/teacher-go-off/', views_class.ClassExitTeacher.as_view({'delete': 'exit_teacher_auto'}), name='teacher-go-off-auto'),
    #Class Apoderados
    path('apoderados/subjects/<int:subject_pk>/class-date/<str:date>/', views_class.Subjects_Apoderados_Class_allView.as_view({'get': 'list'}), name='subject-apoderados-allClass-of-day'),
    path('apoderados/subjects/<int:subject_pk>/class/<int:class_pk>/students-auto/', views_class.ClassStudentAuto.as_view({'post': 'post_student_auto', 'delete': 'delete_student_auto'}), name='subject-add-alumno-auto'),
    path('apoderados/subjects/<int:subject_pk>/class/', views_class.Apoderados_Subject_Class_Get.as_view({'get': 'list_class'}), name='apoderados-subject-class'),
    path('apoderados/subjects/<int:subject_pk>/class/<int:class_pk>/', views_class.Apoderados_Subjects_Class_Retrieve.as_view({'get': 'retrieve_class'}), name='apoderados-class-detail'),
   
    #Use Subject for validate teacher is staff of the subject
    path('subjects/<int:subject_pk>/class/<int:class_pk>/', views_class.ClassInstance_allView.as_view({'get': 'retrieve_class', 'patch': 'patch_class', 'delete': 'delete_class'}), name='clase-detail'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/students/', views_class.ClassStudents.as_view({'get': 'get_students', 'post': 'post_student'}), name='class-add-alumno'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/students/<int:student_pk>/', views_class.ClassStudents.as_view({'delete': 'delete_student'}), name='class-remove-alumno'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/no-students/', views_class.ClassStudents.as_view({'get': 'get_no_students'}), name='class-no-student'),
    #Attendance
    path('subjects/<int:subject_pk>/class/<int:class_pk>/attendances/', views_attendances.Attendances_allView.as_view({'get': 'list_attendances', 'post': 'create_attendance'}), name='asistencia-list'),
    path('subjects/<int:subject_pk>/attendances/<int:attendance_pk>/', views_attendances.Attendances_allView.as_view({'get': 'retrieve_attendance', 'put': 'update_attendance', 'delete': 'delete_attendance'}), name='asistencia-detail'),
    #Attendance Apoderados
    path('apoderados/attendances/<int:attendance_pk>/',views_attendances.AttendanceViewSet.as_view({'patch':'student_update_attendance'}),name='student-change-previous-state'),
   
    #Requests Subjects
    path('subjects/<int:subject_pk>/requests/', views_requests.Requests_GetPatch.as_view({'get': 'list_requests'}), name='list-requests'),
    path('subjects/<int:subject_pk>/requests/<int:request_pk>/', views_requests.Requests_GetPatch.as_view({'patch': 'patch_request'}), name='patch-requests'),
    path('subjects/<int:subject_pk>/requests/<int:request_pk>/acceptordeny-subject/', views_requests.Requests_GetPatch.as_view({'patch': 'acceptordeny_subject_request'}), name='acceptordeny-subject-requests'),
    
    #Requests Class
    path('subjects/<int:subject_pk>/class/<int:class_pk>/requests/', views_requests.Requests_ClassGetPatch.as_view({'get': 'list_requests'}), name='list-requests'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/requests/<int:request_pk>/', views_requests.Requests_ClassGetPatch.as_view({'patch': 'patch_request'}), name='patch-requests'),
    path('subjects/<int:subject_pk>/class/<int:class_pk>/requests/<int:request_pk>/acceptordeny-subject/', views_requests.Requests_ClassGetPatch.as_view({'patch': 'acceptordeny_class_request'}), name='acceptordeny-subject-requests'),
    
    #Hacer URL que devuelva la cantidad de asistencias e inasistencias de un alumno
    #path('asistencias/<int:alumno_pk>/'),
    #path('class/<int:class_pk>/attendances/create-default/', views_attendances.AttendanceOfClass.as_view({'post': 'create_default'}), name='asistencia-create-default'),
    #El de arriba esta bien crea todas las asistencias de los alumnos del horario pero el horario lo consigue la funcion
    #path('courses/<int:course_pk>/subjectss2/', views_subjects_2.Subjects_allView.as_view({'get': 'list'}), name='subjects-list2'),
    #path('all-subjects/', SubjectsView.as_view({'get': 'all_subjects'}), name='all-subjects'),
    #Report
    path('subjects/<int:subject_pk>/info-mail/',views_reports.subject_attendance_info_mail, name='subject-attendance-info-mail'),
    path('subjects/<int:subject_pk>/info/',views_reports.subject_attendance_info, name='subject-attendance-info'),
   
]