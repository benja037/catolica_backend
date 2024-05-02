from rest_framework import serializers
from .models import Clase, Courses, GrupoAlumnos, Teachers, User
from rest_framework.validators import ValidationError
from rest_framework import status

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
class SpecialTeacherSerializer(serializers.ModelSerializer):   
    class Meta:
        model= Teachers
        fields=['id','firstname','lastname']

class CourseSerializer(serializers.ModelSerializer):    
    class Meta:
            model= Courses
            fields=['id','course_name']


class StudentsSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    class Meta:
        model= Students
        fields=['id','admin','gender','date_of_birth','firstname','lastname']
class SimpleStudentsSerializer(serializers.ModelSerializer):    
    class Meta:
        model= Students
        fields=['id','firstname','lastname']

#----------Subjects Serializer-------------------
#Get all subjects
class SubjectsRetrieveSerializer(serializers.ModelSerializer):  
    profesores = TeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subjects
        fields=['id','subject_name','profesores','course_id','num_max_alumnos','public','finished']#Falta alumnos

class SubjectsPostSerializer(serializers.ModelSerializer):  
    profesores = SpecialTeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subjects
        fields=['id','subject_name','profesores','course_id','num_max_alumnos','public','finished']

class SubjectsPatchSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Subjects
        fields=['id','subject_name','num_max_alumnos','public','finished']    

    
class SubjectsGetSerializer(serializers.ModelSerializer):  
    profesores = SpecialTeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subjects
        fields=['id','subject_name','profesores','course_id','num_max_alumnos','public','finished']
    def get_student(self,request):        
        try:
            teacher = Students.objects.get(admin=request.user)            
            return teacher
        except Students.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 
        
    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except Teachers.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.user_type == 'alumno':
            # Verificar si el alumno está inscrito
            alumno_id = self.get_student(request)
            alumnos_inscritos = [alumno['id'] for alumno in representation['alumnos']]
            if alumno_id.id in alumnos_inscritos:
                representation['rolled'] = True
            else:
                representation['rolled'] = False
        if request and request.user.user_type == 'profesor':
            # Verificar si el alumno está inscrito
            teacher_id = self.get_teacher(request)
            teachers_inscritos = [teacher['id'] for teacher in representation['profesores']]
            if teacher_id.id in teachers_inscritos:
                representation['rolled'] = True            
            else:
                representation['rolled'] = False
        return representation


#Get specific subject
class Subjects_with_students_Serializer(serializers.ModelSerializer):
    alumnos = StudentsSerializer(many=True, read_only=True)
    profesores = TeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subjects
        fields=['id','subject_name','profesores','alumnos']
        
    def get_student(self,request):        
        try:
            teacher = Students.objects.get(admin=request.user)            
            return teacher
        except Students.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 
        
    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except Teachers.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.user_type == 'alumno':
            # Verificar si el alumno está inscrito
            alumno_id = self.get_student(request)
            alumnos_inscritos = [alumno['id'] for alumno in representation['alumnos']]
            if alumno_id.id in alumnos_inscritos:
                representation['rolled'] = True
            else:
                representation['rolled'] = False
        if request and request.user.user_type == 'profesor':
            # Verificar si el alumno está inscrito
            teacher_id = self.get_teacher(request)
            teachers_inscritos = [teacher['id'] for teacher in representation['profesores']]
            if teacher_id.id in teachers_inscritos:
                representation['rolled'] = True            
            else:
                representation['rolled'] = False
        return representation
#Update specific subject
class Subjects_all_edit(serializers.ModelSerializer):
    profesores = TeacherSerializer(many=True, read_only=True)  
    alumnos = StudentsSerializer(many=True, read_only=True)
    class Meta:
        model = Subjects
        fields=['id','subject_name','profesores','alumnos','finished']


class AddSubjectsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Subjects
        fields=['course_id','subject_name','profesores']

class ClaseSerializer(serializers.ModelSerializer):
    staff_id = TeacherSerializer(read_only=True)
    class Meta:
        model = Clase
        fields=['id','subject_id','date','time_start','time_end','estado','staff_id','num_max_alumnos','public','etiqueta']

class GrupoAlumnosSerializer(serializers.ModelSerializer):
    alumnos = StudentsSerializer(many=True, read_only=True)
    class Meta:
        model = GrupoAlumnos
        fields=['id','subject_id','name','alumnos']

""" class GrupoAlumnos_with_studentes_Serializer(serializers.ModelSerializer):
    alumnos_horario = StudentsSerializer(many=True, read_only=True)
    class Meta:
        model = GrupoAlumnos
        fields=['id','day_of_week','time','alumnos','subject_id'] """
        
""" def get_student(self,request):        
        try:
            teacher = Students.objects.get(admin=request.user)            
            return teacher
        except Students.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 
        
    def get_teacher(self,request):        
        try:
            teacher = Teachers.objects.get(admin=request.user)            
            return teacher
        except Teachers.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.user_type == 'alumno':
            # Verificar si el alumno está inscrito
            alumno_id = self.get_student(request)
            alumnos_inscritos = [alumno['id'] for alumno in representation['alumnos_horario']]
            if alumno_id.id in alumnos_inscritos:
                representation['rolled'] = True
            else:
                representation['rolled'] = False """
    
""" if request and request.user.user_type == 'profesor':
            # Verificar si el alumno está inscrito
            teacher_id = self.get_teacher(request)
            #alumnos_inscritos = [alumno['id'] for alumno in representation['alumnos']]
            if teacher_id.id == representation['staff_id']:
                representation['rolled'] = True
            else:
                representation['rolled'] = False
        return representation """

class AttendanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Attendance
        fields=['id','student_id','clase_id','estado','user_estado_previo']


class AttendanceSerializerNameLastname(serializers.ModelSerializer):
    user_estado_previo =serializers.ReadOnlyField()
    student = SimpleStudentsSerializer(source='student_id', read_only=True)
    class Meta:
        model = Attendance
        fields=['id','student','clase_id','estado','user_estado_previo']
class AttendanceSerializerOnlyEstadoChange(serializers.ModelSerializer):        
    user_estado_previo =serializers.ReadOnlyField()    
    class Meta:
        model = Attendance
        fields=['id','student_id','clase_id','estado','user_estado_previo']


#===============================================================================
class SignUpSerializer(serializers.ModelSerializer):    
    email= serializers.CharField(max_length=80)
    username=serializers.CharField(max_length=45)
    password=serializers.CharField(min_length=8,write_only=True)
    firstname=serializers.CharField(max_length=45)
    lastname=serializers.CharField(max_length=45)
    date_of_birth = serializers.DateField()
    user_type=serializers.CharField(max_length=10)
    gender=serializers.CharField(max_length=20)
 
    class Meta:
        model=User
        fields= ['email','username','password','firstname','lastname','date_of_birth','user_type','gender']

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
            
            

        