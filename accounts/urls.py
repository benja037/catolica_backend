from . import views
from . import views_simple
from . import views_subjects
from . import views_courses
from . import views_subjects_2
from . import views_horarios
from . import views_clases
from . import views_asistencias
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,  TokenVerifyView)
#from .views import EjemploVista,TuModeloDetalle
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'subjects',views_simple.SubjectsView, 'subject')
router.register(r'students',views_simple.StudentsView, 'student')
router.register(r'users',views_simple.UserView, 'user')
router.register(r'attendance',views_simple.AttendanceView, 'attendance')
#router.register(r'courses',views_simple.CoursesView, 'courses')
router.register(r'horario',views_simple.HorarioView, 'horario')


#router.register(r'subjectss',views_subjects.Subjects_allView, 'subjectss')



urlpatterns = [    
    path("listar/",include(router.urls)),
    #path('ejemplo/', EjemploVista.as_view(), name='ejemplo'),
    #path('obj/<int:pk>/', TuModeloDetalle.as_view(), name='obj'),
    path('listar/subjects/<int:subject_id>/attendance/', views.SubjectAttendanceAPIView.as_view(), name='subject_attendance_api'),
    #path('probando/', views.ProbandoAPIView.as_view(), name='subject_attendance_api'),
    path('mysubjects/', views.SubjectbyAPIView.as_view(), name='subject_attendance_api'),

    #path('clases/alumnos/', ListaAlumnosClaseAPIView.as_view(), name='lista_alumnos_clase'),
    #path("api/",include(router.urls))
    #path('subjects/', SubjectsView.as_view(), name='subjects'),
    path('courses/<int:course_pk>/subjectss/', views_subjects.Subjects_allView.as_view({'get': 'list_subjects', 'post': 'create_subject'}), name='subjects-list'),
    path('courses/<int:course_pk>/subjectss/<int:pk>/', views_subjects.Subjects_allView.as_view({'get': 'retrieve_subject', 'put': 'update_subject', 'delete': 'delete_subject'}), name='subject-detail'),
    #Falta cambiar el de arriba
    path('subjects/<int:pk>/alumnos/', views_subjects.SubjectsAlumnos.as_view({'get': 'get_alumnos', 'post': 'post_alumno', 'delete': 'delete_alumno'}), name='subject-add_alumno'),

    path('subjects/<int:pk>/alumnos-auto/', views_subjects.SubjectsAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),

    path('courses/', views_courses.Courses_allView.as_view({'get': 'list_courses', 'post': 'create_course'}), name='courses-list'),
    path('courses/<int:course_pk>/', views_courses.Courses_allView.as_view({'get': 'retrieve_courses', 'put': 'update_course', 'delete': 'delete_course'}), name='subject-detail'),

     
    path('subjectss/<int:pk>/horarios/', views_horarios.Horarios_allView.as_view({'get': 'list_horarios', 'post': 'create_horario'}), name='horario-list'),
    path('horarios/<int:horario_pk>/', views_horarios.Horarios_allView.as_view({'get': 'retrieve_horario', 'put': 'update_horario', 'delete': 'delete_horario'}), name='horario-detail'),
    #Ultimo cambio se saca subjects para ver el id de un horario, al parecer despues hay que hacer lo mismo con las otras urls
    path('horarios/<int:horario_pk>/alumnos/', views_horarios.CursoMateriaAlumnos.as_view({'get': 'get_alumnos', 'post': 'post_alumno', 'delete': 'delete_alumno'}), name='horario-add_alumno'),
    #Este delete pide "alumno_pk"
    path('horarios/<int:horario_pk>/alumnos-auto/', views_horarios.HorarioAlumnosAuto.as_view({'post': 'post_alumno_auto', 'delete': 'delete_alumno_auto'}), name='horario-add_alumno'),

    
    
    
    path('subjects/<int:subject_pk>/horarios/clases/', views_clases.Subjects_Clases_allView.as_view({'get': 'list'}), name='subject-allHorarios-clase-list'),
    path('horarios/<int:horario_pk>/clases/', views_clases.Clases_allView.as_view({'get': 'list_clases', 'post': 'create_clase'}), name='clase-list'),
    path('clases/<int:clase_pk>/', views_clases.Clases_allView.as_view({'get': 'retrieve_clase', 'put': 'update_clase', 'delete': 'delete_clase'}), name='clase-detail'),

    path('clases/<int:clase_pk>/asistencias/', views_asistencias.Asistencias_allView.as_view({'get': 'list_asistencias', 'post': 'create_asistencia'}), name='asistencia-list'),
    path('asistencias/<int:asistencia_pk>/', views_asistencias.Asistencias_allView.as_view({'get': 'retrieve_asistencia', 'put': 'update_asistencia', 'delete': 'delete_asistencia'}), name='asistencia-detail'),
    #Hacer URL que devuelva la cantidad de asistencias e inasistencias de un alumno
    #path('asistencias/<int:alumno_pk>/'),
    path('clases/<int:clase_pk>/asistencias/create-default/', views_asistencias.AttendanceOfClass.as_view({'post': 'create_default'}), name='asistencia-create-default'),
    #El de arriba esta bien crea todas las asistencias de los alumnos del horario pero el horario lo consigue la funcion
    #path('courses/<int:course_pk>/subjectss2/', views_subjects_2.Subjects_allView.as_view({'get': 'list'}), name='subjects-list2'),
    #path('all-subjects/', SubjectsView.as_view({'get': 'all_subjects'}), name='all-subjects'),

]