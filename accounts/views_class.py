from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import  IsOwnerofStudent, IsProfesorOfSubjectOrReadOnly, IsProfesorOrReadOnly
from accounts.serializers import ClassInstancePutSerializer, ClassInstanceSerializer, ClassRetrieveApoderadoSerializer, StudentSerializer

from .models import Attendance, Discipline, StudentClassRequest, StudentGroup, Student,Subject,ClassInstance, Teacher, CustomUser
from rest_framework.permissions import IsAuthenticated

#List [ID,subject_name,staff_id] /subjectss/
@permission_classes([IsProfesorOfSubjectOrReadOnly])
class ClassInstance_allView(ModelViewSet):    
    serializer_class = ClassInstanceSerializer       
    queryset = ClassInstance.objects.all()
    def get_queryset(self):
        subject_pk = self.request.query_params.get('subject_pk') or None
        if subject_pk is not None:
            classInstances = ClassInstance.objects.filter(subject=subject_pk)             
            serializer = self.serializer_class(classInstances, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_class(self, class_id):
        try:
            return ClassInstance.objects.get(id=class_id)
        except ClassInstance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_class(self,request,subject_pk=None):
        try:
            classInstances = ClassInstance.objects.filter(subject=subject_pk) 
            serializer = ClassInstanceSerializer(classInstances, many=True)
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        
    @action(detail=True, methods=['get'])    
    def retrieve_class(self, request,class_pk=None,subject_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            serializer = ClassInstanceSerializer(classInstance)
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=False, methods=['post'])
    def create_class(self, request,subject_pk=None):
        group_id = request.data.get('group_id', None)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            teacher = self.get_teacher(request)
            class_instance =serializer.save(subject=Subject.objects.get(id=subject_pk))
            class_instance.teachers.add(teacher)
            if group_id != None and group_id != "":
                class_instance.add_students_group(group_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'])
    def delete_class(self, request,class_pk=None,subject_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            classInstance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['patch'])
    def patch_class(self, request,class_pk=None,subject_pk=None):
        try:
            classInstance = self.get_class(class_id=class_pk)
            serializer = ClassInstancePutSerializer(classInstance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) #Hay que arreglar los errores las excepciones
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
#Show class from a specific day        
@permission_classes([IsProfesorOrReadOnly])
class Subjects_Class_allView(ModelViewSet):
    serializer_class = ClassInstanceSerializer
    queryset = ClassInstance.objects.all()
    
    def list(self,request,subject_pk=None,date=None):
        try:       
            classInstances = ClassInstance.objects.filter(subject=subject_pk, date=date).order_by('time_start')            
            class_data = ClassInstanceSerializer(classInstances, many=True).data                
            return Response(class_data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


        

@permission_classes([IsProfesorOfSubjectOrReadOnly])
class ClassStudents(ModelViewSet):
    def get_students(self, request, class_pk=None,subject_pk=None):
        try:
            classinstance = ClassInstance.objects.get(id=class_pk)
            serializer = StudentSerializer(classinstance.students,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ClassInstance.DoesNotExist:
            return Response({"message": "Class no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    def get_no_students(self, request, subject_pk=None,class_pk=None):
        try:
            subject = Subject.objects.get(id=subject_pk)
            classinstance = ClassInstance.objects.get(id=class_pk)
            students_of_class = classinstance.students.all()
            students_of_subject = subject.students.all()
            students_out_class = [student for student in students_of_subject if student not in students_of_class]
            serializer = StudentSerializer(students_out_class,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_student(self, request, class_pk=None,subject_pk=None):
        try:            
            student_pk = request.data.get('student_pk')  
            student = Student.objects.get(id=student_pk)
            classinstance = ClassInstance.objects.get(id=class_pk)
            if classinstance.num_max_students <= len(classinstance.students.all()):                
                return Response(data={
                "message": "Lleno"}, status=status.HTTP_400_BAD_REQUEST)
            
            classinstance.students.add(student)
            Attendance.objects.create(class_instance=classinstance, student=student, state=False)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)                
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_student(self,request, class_pk=None,student_pk=None,subject_pk=None):
        try:                       
            student = Student.objects.get(id=student_pk)
            classinstance = ClassInstance.objects.get(id=class_pk)
            classinstance.students.remove(student)
            #Attendances of classinstance, maybe need a if
            Attendance.objects.filter(class_instance=classinstance, student=student).delete()       

            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated,IsProfesorOfSubjectOrReadOnly])
class SubjectsExitTeacher(ModelViewSet):
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def exit_teacher_auto(self,request, subject_pk=None):
        try:
            teacher = self.get_teacher(request)
            subject = Subject.objects.get(id=subject_pk)
            subject.teachers.remove(teacher)
            classInstances = ClassInstance.objects.filter(subject=subject,estado='proximamente')
            for classInstance in classInstances:
                if (teacher in classInstance.teachers.all()):
                    classInstance.teachers.remove(teacher)
            return Response({"message": "Teacher eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)       
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)@permission_classes([IsAuthenticated,IsProfesorOfSubjectOrReadOnly])

@permission_classes([IsAuthenticated,IsProfesorOfSubjectOrReadOnly])
class ClassExitTeacher(ModelViewSet):
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except CustomUser.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def exit_teacher_auto(self,request, subject_pk=None):
        try:
            teacher = self.get_teacher(request)
            classInstance = Subject.objects.get(id=subject_pk)
            classInstance.teachers.remove(teacher)            
            return Response({"message": "Teacher eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)       
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
#APODERADOS
#Views Apoderados
#Show class from a specific day        
@permission_classes([IsOwnerofStudent])
class Subjects_Apoderados_Class_allView(ModelViewSet):
    serializer_class = ClassRetrieveApoderadoSerializer
    queryset = ClassInstance.objects.all()
    
    def list(self,request,subject_pk=None,date=None):
        try:       
            classInstances = ClassInstance.objects.filter(subject=subject_pk, date=date).order_by('time_start')            
            class_data = ClassRetrieveApoderadoSerializer(classInstances,context={'request':request}, many=True).data                
            return Response(class_data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsOwnerofStudent])
class ClassStudentAuto(ModelViewSet):
    def get_student(self,request):        
        try:
            profile_id = request.data.get('profile_id')
            print("profile_id",profile_id)
            student = Student.objects.get(id=profile_id)         #Falta poner que si es profesor no pueda usar esta vista  
            return student
        except Student.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def post_student_auto(self, request, subject_pk=None,class_pk=None):
        try:            
            student = self.get_student(request)              
            class_instance = ClassInstance.objects.get(id=class_pk)
            if class_instance.mode == 'privado':
                return Response({"message": "No puedes agregar estudiantes a una clase privada"}, status=status.HTTP_403_FORBIDDEN)
            if class_instance.mode == 'moderado':
                requests_earrings = StudentClassRequest.objects.filter(student=student, class_instance=class_instance,state='pendiente')
                if requests_earrings :
                    return Response({"message": "ya enviaste la solicitud"}, status=status.HTTP_403_FORBIDDEN)
                else:
                    StudentClassRequest.objects.create(student=student, class_instance=class_instance,state='pendiente')
                    return Response({"message": "Solicitud enviada correctamente"}, status=status.HTTP_201_CREATED)
                #return Response({"message": "No puedes agregar estudiantes a un subject moderado"}, status=status.HTTP_403_FORBIDDEN)            
            class_instance.students.add(student)
            return Response({"message": "Estudiante agregado correctamente"}, status=status.HTTP_201_CREATED)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ClassInstance.DoesNotExist:
            return Response({"message": "Clase no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_student_auto(self,request, subject_pk=None,class_pk=None):
        try:
            student = self.get_student(request)
            class_instance = ClassInstance.objects.get(id=class_pk)
            class_instance.students.remove(student)
            return Response({"message": "Estudiante eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except ClassInstance.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
@permission_classes([IsOwnerofStudent])
class Apoderados_Subject_Class_Get(ModelViewSet):    
    serializer_class = ClassRetrieveApoderadoSerializer       
    queryset = ClassInstance.objects.all()    
    
    @action(detail=True, methods=['get']) 
    def list_class(self,request,subject_pk=None):
        try:
            class_of_subject = ClassInstance.objects.get(id=subject_pk)
            serializer = ClassRetrieveApoderadoSerializer(class_of_subject, many=True,context={'request':request})
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        
@permission_classes([IsOwnerofStudent])
class Apoderados_Subjects_Class_Retrieve(ModelViewSet):    
    serializer_class = ClassRetrieveApoderadoSerializer       
    queryset = ClassInstance.objects.all()

    def get_class(self, class_id):
        try:
            return ClassInstance.objects.get(id=class_id)
        except ClassInstance.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
   
    
    @action(detail=True, methods=['get'])    
    def retrieve_class(self, request, subject_pk=None,class_pk=None):
        try:
            class_instance = self.get_class(class_id=class_pk)
            serializer = ClassRetrieveApoderadoSerializer(class_instance,context={'request':request})
            return Response(serializer.data)
        except ClassInstance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
