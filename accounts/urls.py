from . import views_subjects
from . import views_courses
from . import views_informes
from . import views_grupos
from . import views_clases
from . import views_asistencias

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
    #Courses
    path('courses/', views_courses.Courses_allView.as_view({'get': 'list_courses', 'post': 'create_course'}), name='courses-list'),
    path('courses/<int:course_pk>/', views_courses.Courses_allView.as_view({'get': 'retrieve_courses', 'put': 'update_course', 'delete': 'delete_course'}), name='subject-detail'),
    #Subjects
    path('courses/<int:course_pk>/subjects/', views_subjects.Subjects_allView.as_view({'get': 'list_subjects', 'post': 'create_subject'}), name='subjects-list'),
    path('subjects/<int:pk>/', views_subjects.Subjects_allView.as_view({'get': 'retrieve_subject', 'patch': 'update_subject', 'delete': 'delete_subject'}), name='subject-detail'),
    path('subjects/<int:pk>/alumnos/', views_subjects.SubjectsAlumnos.as_view({'get': 'get_alumnos', 'post': 'post_alumno', 'delete': 'delete_alumno'}), name='subject-add_alumno'),
    path('subjects/<int:pk>/alumnos-auto/', views_subjects.SubjectsAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),
    #    
    path('subjects/<int:pk>/grupos/', views_grupos.Grupos_allView.as_view({'get': 'list_grupos', 'post': 'create_grupo'}), name='grupo-list'),
    path('grupos/<int:grupo_pk>/', views_grupos.Grupos_allView.as_view({'get': 'retrieve_grupo', 'put': 'update_grupo', 'delete': 'delete_grupo'}), name='grupo-detail'),
    #Ultimo cambio se saca subjects para ver el id de un horario, al parecer despues hay que hacer lo mismo con las otras urls
    path('grupos/<int:grupo_pk>/alumnos/', views_grupos.CursoMateriaAlumnos.as_view({'get': 'get_alumnos', 'post': 'post_alumno', 'delete': 'delete_alumno'}), name='horario-add_alumno'),
    #Este delete pide "alumno_pk"
    #ACA se elimina porque los grupos ahora pasan solo a ser de utilidad a los profesores
    #path('grupos/<int:grupo_pk>/alumnos-auto/', views_grupos.HorarioAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),

    
    
    
    path('subjects/<int:pk>/clases/<str:date>/', views_clases.Subjects_Clases_allView.as_view({'get': 'list'}), name='subject-allHorarios-clase-list'),
    path('subjects/<int:pk>/clases/', views_clases.Clases_allView.as_view({'get': 'list_clases', 'post': 'create_clase'}), name='clase-list'),
    path('clases/<int:clase_pk>/', views_clases.Clases_allView.as_view({'get': 'retrieve_clase', 'put': 'update_clase', 'delete': 'delete_clase'}), name='clase-detail'),

    path('clases/<int:clase_pk>/asistencias/', views_asistencias.Asistencias_allView.as_view({'get': 'list_asistencias', 'post': 'create_asistencia'}), name='asistencia-list'),
    path('asistencias/<int:asistencia_pk>/', views_asistencias.Asistencias_allView.as_view({'get': 'retrieve_asistencia', 'put': 'update_asistencia', 'delete': 'delete_asistencia'}), name='asistencia-detail'),
    #Hacer URL que devuelva la cantidad de asistencias e inasistencias de un alumno
    #path('asistencias/<int:alumno_pk>/'),
    path('clases/<int:clase_pk>/asistencias/create-default/', views_asistencias.AttendanceOfClass.as_view({'post': 'create_default'}), name='asistencia-create-default'),
    #El de arriba esta bien crea todas las asistencias de los alumnos del horario pero el horario lo consigue la funcion
    #path('courses/<int:course_pk>/subjectss2/', views_subjects_2.Subjects_allView.as_view({'get': 'list'}), name='subjects-list2'),
    #path('all-subjects/', SubjectsView.as_view({'get': 'all_subjects'}), name='all-subjects'),
    path('informe/subjects/<int:pk>/',views_informes.subject_attendance_info, name='subject-attendance-info'),
   
]