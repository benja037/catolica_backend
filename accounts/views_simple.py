from rest_framework.viewsets import ModelViewSet

from accounts.models import Attendance, Courses, GrupoAlumnos, Students, Subjects, User
from accounts.serializers import AttendanceSerializer, CourseSerializer, GrupoAlumnosSerializer, StudentsSerializer, SubjectsSerializer, UserSerializer



#=================================Simple Views==========================================
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []    

class SubjectsView(ModelViewSet):
    queryset = Subjects.objects.all()
    serializer_class = SubjectsSerializer
    permission_classes = []

class StudentsView(ModelViewSet):
    queryset = Students.objects.all()
    serializer_class = StudentsSerializer
    permission_classes = []

class AttendanceView(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = []

class CoursesView(ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CourseSerializer
    permission_classes = []

class GrupoAlumnosView(ModelViewSet):
    queryset = GrupoAlumnos.objects.all()
    serializer_class = GrupoAlumnosSerializer
    permission_classes = []

    