from rest_framework import serializers
from .models import User
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
        fields=['id','firstname','lastname','date_of_birth']

class StudentsSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model= Students
        fields=['id','admin','gender','address']


class SubjectsSerializer(serializers.ModelSerializer):
    alumnos = StudentsSerializer(many=True, read_only=True)
    class Meta:
        model = Subjects
        fields=['id','subject_name','course_id','staff_id','alumnos']

class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields=['id','student_id','subject_id','estado','dateandhour']

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
            
            

        