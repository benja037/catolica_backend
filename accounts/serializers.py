from rest_framework import serializers
from .models import Clase, Teachers, User
from rest_framework.validators import ValidationError


from .models import Students, Subjects,Attendance

""" class AlumnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = ('id')  # Puedes incluir más campos si es necesario

class ClaseAlumnosSerializer(serializers.ModelSerializer):
    #alumnos = AlumnoSerializer(many=True)

    class Meta:
        model = Subjects
        fields = ('id','subject_name')  # Incluye más campos si es necesario """

#===========================simple serializer========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields=['id','email','username','gender','date_of_birth','firstname','lastname','phone_number','user_type']

class TeacherSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model= Teachers
        fields=['id','admin','gender','date_of_birth','firstname','lastname']

class CourseSerializer(serializers.ModelSerializer):    
    class Meta:
            model= Students
            fields=['id','course_name']


class StudentsSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model= Students
        fields=['id','admin','gender','date_of_birth','firstname','lastname']


class SubjectsSerializer(serializers.ModelSerializer):
    alumnos = StudentsSerializer(many=True, read_only=True)
    class Meta:
        model = Subjects
        fields=['id','subject_name','staff_id','alumnos']

class AddSubjectsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subjects
        fields=['course_id','subject_name','staff_id']

class ClaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clase
        fields=['id','subject_name','date_and_hour','subject_id','estado']

class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields=['id','student_id','subject_id','estado','dateandhour']


class AttendanceSerializerOnlyDateandHour(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields=['dateandhour']
#===============================================================================
class SignUpSerializer(serializers.ModelSerializer):    
    email= serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=45)
    password=serializers.CharField(min_length=8,write_only=True)
    firstname=serializers.CharField(max_length=45)
    lastname=serializers.CharField(max_length=45)
    date_of_birth = serializers.DateField()
    user_type=serializers.CharField(max_length=10)
 
    class Meta:
        model=User
        fields= ['email','username','password','firstname','lastname','date_of_birth','user_type']

    def validate(self,attrs):
        email_exists=User.objects.filter(email=attrs['email']).exists()
            
        if email_exists:
            raise ValidationError("Email has already been used")
        
        return super().validate(attrs)
    
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)

        user.set_password(password)
        user.save()

        return user
            
            

        