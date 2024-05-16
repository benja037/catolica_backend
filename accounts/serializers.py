from rest_framework import serializers
from .models import ClassInstance, Discipline, StudentGroup, StudentSubjectRequest, Teacher, CustomUser,Student,Subject,Attendance
from rest_framework.validators import ValidationError
from rest_framework import status

#===========================simple serializer========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= CustomUser
        fields=['id','email','gender','date_of_birth','firstname','lastname','phone_number','user_type']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model= Teacher
        fields=['id','user','gender','date_of_birth','firstname','lastname']

class SpecialTeacherSerializer(serializers.ModelSerializer):   
    class Meta:
        model= Teacher
        fields=['id','firstname','lastname']

class DisciplineSerializer(serializers.ModelSerializer):    
    class Meta:
            model= Discipline
            fields=['id','discipline_name']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model= Student
        fields=['id','user','gender','date_of_birth','firstname','lastname','phone_number','document_type','document_number']

class SimpleStudentSerializer(serializers.ModelSerializer):    
    class Meta:
        model= Student
        fields=['id','firstname','lastname']

#----------Subjects Serializer-------------------
#subjects/<int:pk>/
class SubjectRetrieveSerializer(serializers.ModelSerializer):  
    teachers = TeacherSerializer(many=True, read_only=True)
    students = StudentSerializer(many=True, read_only=True)  
    class Meta:
        model = Subject
        fields=['id','subject_name','teachers','students','discipline','num_max_students','mode','finished']
    def get_student(self,request):        
        try:
            student = Student.objects.get(user=request.user)            
            return student
        except Student.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 
        
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')        
        if request and request.user.user_type == 'alumno':            
            student = self.get_student(request)
            id_of_students = [student['id'] for student in representation['students']]
            if student.id in id_of_students:
                representation['rolled'] = True
            else:
                representation['rolled'] = False
        if request and request.user.user_type == 'profesor':           
            teacher = self.get_teacher(request)
            id_of_teachers = [teacher['id'] for teacher in representation['teachers']]
            if teacher.id in id_of_teachers:
                representation['rolled'] = True            
            else:
                representation['rolled'] = False
        return representation
    
#courses/<int:course_pk>/subjects/
class SubjectPostSerializer(serializers.ModelSerializer):  
    teachers = SpecialTeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subject
        fields=['id','subject_name','teachers','discipline','num_max_students','mode','finished']

#subjects/<int:pk>/
class SubjectPatchSerializer(serializers.ModelSerializer):       
    class Meta:
        model = Subject
        fields=['id','subject_name','num_max_students','mode','finished']    

#courses/<int:course_pk>/subjects/
class SubjectGetSerializer(serializers.ModelSerializer):  
    students = SimpleStudentSerializer(many=True,read_only=True)
    teachers = SpecialTeacherSerializer(many=True, read_only=True)  
    class Meta:
        model = Subject
        fields=['id','subject_name','teachers','students','discipline','num_max_students','mode','finished']
    def get_student(self,request):        
        try:
            student = Student.objects.get(user=request.user)            
            return student
        except Student.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 
        
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.user_type == 'alumno':            
            student = self.get_student(request)
            id_of_students = [student['id'] for student in representation['students']]
            if student.id in id_of_students:
                representation['rolled'] = True
            else:
                representation['rolled'] = False
                if representation['mode'] == "moderado":
                    requests_earrings = StudentSubjectRequest.objects.filter(student=student, subject=instance,state='pendiente')
                    if requests_earrings :
                        representation['requests'] = "solicitado"                        
                    else:
                        representation['requests'] = "solicitar"
                 
        if request and request.user.user_type == 'profesor':       
            teacher = self.get_teacher(request)
            id_of_teachers = [teacher['id'] for teacher in representation['teachers']]
            if teacher.id in id_of_teachers:
                representation['rolled'] = True            
            else:
                representation['rolled'] = False
        return representation
#----------ClassInstance Serializer-------------------
class ClassInstanceSerializer(serializers.ModelSerializer):
    teachers = SpecialTeacherSerializer(many=True, read_only=True)  
    students = SimpleStudentSerializer(many=True, read_only=True)
    class Meta:
        model = ClassInstance
        fields=['id','subject','date','time_start','time_end','state','teachers','num_max_students','mode','label','students']

class ClassInstancePutSerializer(serializers.ModelSerializer):    
    class Meta:
        model = ClassInstance
        fields=['id','subject','date','time_start','time_end','state','num_max_students','mode','label']

class StudentGroupSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = StudentGroup
        fields=['id','subject','name','students']
class StudentGroupPostSerializer(serializers.ModelSerializer):    
    class Meta:
        model = StudentGroup
        fields=['id','name']


class AttendanceSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Attendance
        fields=['id','student','class_instance','state','user_previous_state']


class AttendanceSerializerNameLastname(serializers.ModelSerializer):
    user_previous_state =serializers.ReadOnlyField()
    student = SimpleStudentSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields=['id','student','class_instance','state','user_previous_state']
class AttendanceSerializerOnlyStateChange(serializers.ModelSerializer):        
    user_previous_state =serializers.ReadOnlyField()    
    class Meta:
        model = Attendance
        fields=['id','student','class_instance','state','user_previous_state']

class StudentSubjectRequestSerializer(serializers.ModelSerializer):     
    class Meta:
        model = Subject
        fields=['id','subject','student','state']


#===============================================================================
class SignUpSerializer(serializers.ModelSerializer):    
    email= serializers.CharField(max_length=80)
    #username=serializers.CharField(max_length=45)
    password=serializers.CharField(min_length=8,write_only=True)
    firstname=serializers.CharField(max_length=45)
    lastname=serializers.CharField(max_length=45)
    date_of_birth = serializers.DateField()
    user_type=serializers.CharField(max_length=10)
    gender=serializers.CharField(max_length=20)
 
    class Meta:
        model=CustomUser
        fields= ['email','password','firstname','lastname','date_of_birth','user_type','gender']

    def validate(self,attrs):
        email_exists=CustomUser.objects.filter(email=attrs['email']).exists()
            
        if email_exists:
            raise ValidationError("Email has already been used")
        
        return super().validate(attrs)
    
    def create(self,validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)

        user.set_password(password)
        user.save()

        return user
            
            

        