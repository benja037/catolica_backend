import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,permission_classes,api_view

from accounts.permissions import IsProfesorOrReadOnly
from accounts.serializers import StudentSerializer

from .models import Attendance, ClassInstance, StudentGroup, Student,Subject,Discipline, Teacher, CustomUser
from rest_framework.permissions import IsAuthenticated
from openpyxl import Workbook

import os
from django.conf import settings
from django.http import JsonResponse
from django.core.mail import EmailMessage, get_connection

@api_view(['GET'])
@permission_classes([IsProfesorOrReadOnly])
def subject_attendance_info_mail(request, subject_pk):
    try:
        dict_attendance = {}
        
        # Obtener el tema específico
        subject = get_object_or_404(Subject, id=subject_pk)
        
        # Obtener todas las asistencias relacionadas con las clases del tema
        attendances = Attendance.objects.filter(class_instance__subject=subject_pk,class__state ='realizada')

        # Obtener todos los estudiantes del tema
        students = subject.students.all()

        # Crear un nuevo libro de Excel y una hoja de cálculo
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Asistencias"

        for student in students:
            # Filtrar las asistencias del estudiante en las clases del tema
            student_attendances = attendances.filter(student=student.id)

            # Contar las asistencias verdaderas y falsas del estudiante
            attendance_true_count = student_attendances.filter(state=True).count()
            attendance_false_count = student_attendances.filter(state=False).count()
            student_serializer = StudentSerializer(student)

            """ dict_attendance[student_serializer.data['id']] = {
                'firstname': student_serializer.data['firstname'],
                'lastname': student_serializer.data['lastname'],
                'True': attendance_true_count,
                'False': attendance_false_count
            } """
            # Obtener el nombre y apellido del estudiante
            student_name = f"{student.firstname} {student.lastname}"

            # Agregar datos del estudiante a la hoja de cálculo
            sheet.append([student_name, attendance_true_count, attendance_false_count])

        # Crear la respuesta HTTP con el archivo Excel adjunto
        """ response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="asistencias.xlsx"' """
        # Obtener la marca de tiempo actual en milisegundos
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Generar un nombre de archivo único con la marca de tiempo
        file_name = f"asistencias_{timestamp}.xlsx"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        # Guardar el archivo temporalmente en el servidor
        workbook.save(file_path)
        subject = "Hello from Django SMTP"
        recipient_list = ["infoasistencias.ca@gmail.com",]
        from_email = "onboarding@resend.dev"
        message = "<strong>it works!</strong>"

        with get_connection(
            host=settings.RESEND_SMTP_HOST,
            port=settings.RESEND_SMTP_PORT,
            username=settings.RESEND_SMTP_USERNAME,
            password=os.environ["RESEND_API_KEY"],
            use_tls=True,
            ) as connection:
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    to=recipient_list,
                    from_email=from_email,                    
                    connection=connection)
                email.attach_file(file_path)
                email.send()
        return JsonResponse({"status": "ok"})    

    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
@permission_classes([IsProfesorOrReadOnly])
def subject_attendance_info(request, subject_pk):
    try:
        dict_attendance = {}
        
        # Obtener el tema específico
        subject = get_object_or_404(Subject, id=subject_pk)
        
        # Obtener todas las asistencias relacionadas con las clases del tema
        attendances = Attendance.objects.filter(class_instance__subject=subject_pk,class__state ='realizada')

        # Obtener todos los estudiantes del tema
        students = subject.students.all()       

        for student in students:
            # Filtrar las asistencias del estudiante en las clases del tema
            student_attendances = attendances.filter(student=student.id)

            # Contar las asistencias verdaderas y falsas del estudiante
            attendance_true_count = student_attendances.filter(state=True).count()
            attendance_false_count = student_attendances.filter(state=False).count()
            student_serializer = StudentSerializer(student)

            dict_attendance[student_serializer.data['id']] = {
                'firstname': student_serializer.data['firstname'],
                'lastname': student_serializer.data['lastname'],
                'True': attendance_true_count,
                'False': attendance_false_count
            }      
        # Devolver la respuesta con el diccionario de asistencias
        return Response(dict_attendance, status=status.HTTP_200_OK)

    except Subject.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

    