from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes

from accounts.permissions import  IsOwnerofStudent, IsProfesorOfSubjectOrReadOnly,IsProfesorOrReadOnly
from accounts.serializers import  StudentSerializer, SubjectGetApoderadoSerializer, SubjectRetrieveApoderadoSerializer, SubjectRetrieveSerializer, SubjectGetSerializer, SubjectPatchSerializer, SubjectPostSerializer

from .models import Attendance, ClassInstance, Student, StudentSubjectRequest,Subject,Discipline, Teacher, CustomUser,StudentGroup
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsProfesorOrReadOnly])
class Subjects_Get_Post(ModelViewSet):    
    serializer_class = SubjectRetrieveSerializer       
    queryset = Subject.objects.all()
    def get_queryset(self):
        discipline_pk = self.request.query_params.get('discipline_pk') or None
        if discipline_pk is not None:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk)         
            serializer = self.serializer_class(subjects_of_discipline, many=True)
        return Response(serializer.data)


    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    
    def list_subjects(self,request,discipline_pk=None):
        try:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk) 
            serializer = SubjectGetSerializer(subjects_of_discipline, many=True,context={'request':request})
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)        
   
    @action(detail=False, methods=['post'])    
    def create_subject(self, request, discipline_pk=None):
        serializer = SubjectPostSerializer(data=request.data)
        if serializer.is_valid():
            teacher = self.get_teacher(request)
            discipline = Discipline.objects.get(id=discipline_pk)  
           
            subject = serializer.save(discipline=discipline)  
           
            subject.teachers.add(teacher)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@permission_classes([IsProfesorOfSubjectOrReadOnly])    
class Subjects_Retrieve_Delete_Patch(ModelViewSet):
    serializer_class = SubjectRetrieveSerializer       
    queryset = Subject.objects.all()
    def get_queryset(self):
        discipline_pk = self.request.query_params.get('discipline_pk') or None
        if discipline_pk is not None:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk)         
            serializer = self.serializer_class(subjects_of_discipline, many=True)
        return Response(serializer.data)
    def get_teacher(self,request):        
        try:
            teacher = Teacher.objects.get(user=request.user)            
            return teacher
        except Teacher.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND    
    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
    @action(detail=True, methods=['get'])    
    def retrieve_subject(self, request, subject_pk=None):
        try:
            subject = self.get_subject(subject_id=subject_pk)
            serializer = SubjectRetrieveSerializer(subject,context={'request':request})
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
   
    @action(detail=True, methods=['delete'])
    def delete_subject(self, request, subject_pk=None):
        try:            
            subject = self.get_subject(subject_id=subject_pk)
              
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
            
        except Teacher.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=['patch'])
    def update_subject(self, request, subject_pk=None):
        try:
            subject = self.get_subject(subject_id=subject_pk)
            serializer = SubjectPatchSerializer(subject, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsProfesorOfSubjectOrReadOnly])
class SubjectsStudents(ModelViewSet):
    def get_students(self, request, subject_pk=None):
        try:
            subject = Subject.objects.get(id=subject_pk)
            serializer = StudentSerializer(subject.students,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    def get_no_students(self, request, subject_pk=None):
        try:
            subject = Subject.objects.get(id=subject_pk)
            students_of_subject = subject.students.all()
            students_out_subject = Student.objects.exclude(id__in=[s.id for s in students_of_subject])
            serializer = StudentSerializer(students_out_subject,many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

    def post_student(self, request, subject_pk=None):
        try:            
            student_pk = request.data.get('student_pk')  
            student = Student.objects.get(id=student_pk)
            subject = Subject.objects.get(id=subject_pk)
            if subject.num_max_students <= len(subject.students.all()):                
                return Response(data={
                "message": "Lleno"}, status=status.HTTP_400_BAD_REQUEST)
            
            subject.students.add(student)
            return Response({"message": "Alumno agregado correctamente"}, status=status.HTTP_201_CREATED)                
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    def delete_student(self,request, subject_pk=None,student_pk=None):
        try:                       
            student = Student.objects.get(id=student_pk)
            subject = Subject.objects.get(id=subject_pk)
            subject.students.remove(student)
            groups = StudentGroup.objects.filter(subject=subject)
            for group in groups:
                if (student in group.students.all()):
                    group.students.remove(student)
                group.students.remove(student)
            classInstances = ClassInstance.objects.filter(subject=subject, state="proximamente")
            for classInstance in classInstances:
                if (student in classInstance.students.all()):
                    classInstance.students.remove(student)
                    attendance_of_class = Attendance.objects.filter(student=student,class_instance=classInstance)
                    attendance_of_class.delete()
           
            return Response({"message": "Alumno eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)



    
        
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
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
#Views Apoderados
@permission_classes([IsOwnerofStudent])
class Apoderados_Subject_Post_add(ModelViewSet):
    def get_student(self, student_id):
        try:
            student = Student.objects.get(id=student_id)
            return student
        except Student.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND   
        
    def post_student_auto(self, request, subject_pk=None):
        try: 
            student_id = request.query_params.get('student_id')   
            print("student_id",student_id)        
            student = self.get_student(student_id)              
            subject = Subject.objects.get(id=subject_pk)
            if subject.num_max_students <= len(subject.students.all()):
                if subject.mode == 'privado':
                    return Response({"message": "No puedes agregar estudiantes a un subject privado"}, status=status.HTTP_403_FORBIDDEN)
                if subject.mode == 'moderado':
                    requests_earrings = StudentSubjectRequest.objects.filter(student=student, subject=subject,state='pendiente')
                    if requests_earrings :
                        return Response({"message": "ya enviaste la solicitud"}, status=status.HTTP_403_FORBIDDEN)
                    else:
                        StudentSubjectRequest.objects.create(student=student, subject=subject,state='pendiente')
                        return Response({"message": "Solicitud enviada correctamente"}, status=status.HTTP_201_CREATED)
                    #return Response({"message": "No puedes agregar estudiantes a un subject moderado"}, status=status.HTTP_403_FORBIDDEN)            
                subject.students.add(student)            
                return Response({"message": "Estudiante agregado correctamente"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "El subject esta lleno"}, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND)       
   
        

@permission_classes([IsOwnerofStudent])
class Apoderados_Subject_delete(ModelViewSet):
    def get_student(self, student_id):
        try:
            student = Student.objects.get(id=student_id)
            return student
        except Student.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def delete_student_auto(self, request, subject_pk=None):
        try:
            student_id = request.query_params.get('student_id')
            student = self.get_student(student_id)
            subject = Subject.objects.get(id=subject_pk)
            subject.students.remove(student)
            return Response({"message": "Estudiante eliminado correctamente"}, status=status.HTTP_204_NO_CONTENT)
        except Student.DoesNotExist:
            return Response({"message": "Student no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Subject.DoesNotExist:
            return Response({"message": "Subject no encontrado"}, status=status.HTTP_404_NOT_FOUND) 


#Similar to get subjects of teacher difference in serializer, that check if profile estudent is rolled  
@permission_classes([IsOwnerofStudent])
class Apoderados_Subjects_Get(ModelViewSet):    
    serializer_class = SubjectGetApoderadoSerializer       
    queryset = Subject.objects.all()
    def get_queryset(self):
        discipline_pk = self.request.query_params.get('discipline_pk') or None
        if discipline_pk is not None:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk)         
            serializer = self.serializer_class(subjects_of_discipline, many=True)
        return Response(serializer.data)

    
    def list_subjects(self,request,discipline_pk=None):
        try:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk) 
            serializer = SubjectGetApoderadoSerializer(subjects_of_discipline, many=True,context={'request':request})
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)        
        
@permission_classes([IsOwnerofStudent])
class Apoderados_Subjects_Retrieve(ModelViewSet):    
    serializer_class = SubjectGetApoderadoSerializer       
    queryset = Subject.objects.all()

    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND
        
    def get_queryset(self):
        discipline_pk = self.request.query_params.get('discipline_pk') or None
        if discipline_pk is not None:
            subjects_of_discipline = Subject.objects.filter(discipline=discipline_pk)         
            serializer = self.serializer_class(subjects_of_discipline, many=True)
        return Response(serializer.data)

    
    @action(detail=True, methods=['get'])    
    def retrieve_subject(self, request, subject_pk=None):
        try:
            subject = self.get_subject(subject_id=subject_pk)
            serializer = SubjectRetrieveApoderadoSerializer(subject,context={'request':request})
            return Response(serializer.data)
        except Subject.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
