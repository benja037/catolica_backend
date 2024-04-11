from . import views
from . import views_simple
from . import views_subjects
from . import views_courses
from . import views_subjects_2
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

    path('courses/', views_courses.Courses_allView.as_view({'get': 'list_courses', 'post': 'create_course'}), name='courses-list'),
    path('courses/<int:course_pk>/', views_courses.Courses_allView.as_view({'get': 'retrieve_courses', 'put': 'update_course', 'delete': 'delete_course'}), name='subject-detail'),

    path('courses/<int:course_pk>/subjectss2/', views_subjects_2.Subjects_allView.as_view({'get': 'list'}), name='subjects-list2'),
    #path('all-subjects/', SubjectsView.as_view({'get': 'all_subjects'}), name='all-subjects'),

]