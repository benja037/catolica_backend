from . import views
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,  TokenVerifyView)
from .views import EjemploVista,TuModeloDetalle
from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'subjects',views.SubjectsView, 'subject')
router.register(r'students',views.StudentsView, 'student')
router.register(r'users',views.UserView, 'user')
router.register(r'attendance',views.AttendanceView, 'attendance')
router.register(r'courses',views.CoursesView, 'courses')
router.register(r'horario',views.HorarioView, 'horario')

urlpatterns = [    
    path("listar/",include(router.urls)),
    path('ejemplo/', EjemploVista.as_view(), name='ejemplo'),
    path('obj/<int:pk>/', TuModeloDetalle.as_view(), name='obj'),
    path('listar/subjects/<int:subject_id>/attendance/', views.SubjectAttendanceAPIView.as_view(), name='subject_attendance_api'),
    path('probando/', views.ProbandoAPIView.as_view(), name='subject_attendance_api'),
    path('mysubjects/', views.SubjectbyAPIView.as_view(), name='subject_attendance_api'),

    #path('clases/alumnos/', ListaAlumnosClaseAPIView.as_view(), name='lista_alumnos_clase'),
    #path("api/",include(router.urls))
    #path('subjects/', SubjectsView.as_view(), name='subjects'),

]