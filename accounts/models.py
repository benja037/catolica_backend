from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.admin.models import LogEntry as BaseLogEntry
from django.contrib.auth import get_user_model
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        email = self.normalize_email(email)

        user = self.model(
            email = email,
            **extra_fields
        )

        user.set_password(password)
        
        user.save()

        return user

    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email,password,**extra_fields)

class CustomUser(AbstractUser):  
    username = None 

    GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
      
    
    REQUIRED_FIELDS = ['firstname', 'lastname', 'gender']
    USUARIO_ALUMNO = 'alumno'
    USUARIO_PROFESOR = 'profesor'
    USUARIO_APODERADO = 'apoderado'
    USUARIO_ADMIN = 'admin'
    TIPO_USUARIO_CHOICES = [(USUARIO_ALUMNO, 'alumno'),(USUARIO_PROFESOR, 'profesor'),(USUARIO_APODERADO, 'apoderado'),(USUARIO_ADMIN,'admin')] 
    email = models.EmailField(unique=True)  
    gender=models.CharField(choices = GENDER_CHOICES,max_length=15,null = True)      
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    phone_number = models.CharField(max_length=45,null=True)      
    DOCUMENT_CHOICES = [
        ('rut', 'rut'),
        ('pasaporte', 'pasaporte'),
    ]
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=50, null=True)  
    document_number = models.CharField(max_length=50,unique=True)    
    user_type=models.CharField(choices=TIPO_USUARIO_CHOICES,max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    objects= CustomUserManager() 
    def __str__(self):
        return self.email
  
    
class Teacher(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    gender=models.CharField(choices = GENDER_CHOICES,max_length=20,null = True)    
    date_of_birth=models.DateField(null=True)
    phone_number = models.CharField(max_length=45,null=True) 
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
    verified = models.BooleanField(default=False)
    DOCUMENT_CHOICES = [
        ('rut', 'rut'),
        ('pasaporte', 'pasaporte'),
    ]
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=50, null=True)  
    document_number = models.CharField(max_length=50,unique=True)  
    def __str__(self):
        return self.firstname + self.lastname
    

class Discipline(models.Model):
    id=models.AutoField(primary_key=True)
    discipline_name=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.discipline_name


class Student(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True) 
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    DOCUMENT_CHOICES = [
        ('rut', 'rut'),
        ('pasaporte', 'pasaporte'),
    ]
    gender=models.CharField(choices = GENDER_CHOICES,max_length=20,null = True)
    phone_number = models.CharField(max_length=45,null=True)   
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    document_type = models.CharField(choices=DOCUMENT_CHOICES,max_length=50, null=True)  
    document_number = models.CharField(max_length=50,unique=True)  
    def __str__(self):
        return self.firstname + self.lastname
 

class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=50)
    discipline=models.ForeignKey('Discipline',on_delete=models.SET_NULL, null=True)
    teachers=models.ManyToManyField(Teacher)    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(Student)
    num_max_students = models.IntegerField(default=0)
    MODE_CHOICES = [('publico', 'publico'),('privado', 'privado'),('moderado','moderado')]
    mode = models.CharField(choices = MODE_CHOICES,max_length=50,default='moderado')
    finished = models.BooleanField(default=False)


class StudentGroup(models.Model):
    id=models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='groups',blank=True)    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    

class ClassInstance(models.Model):
    id=models.AutoField(primary_key=True)
    subject=models.ForeignKey('Subject', on_delete=models.PROTECT, null=True)
    date= models.DateField()
    time_start = models.TimeField()
    time_end = models.TimeField(null=True)     
    STATE_CHOICES = [('proximamente', 'proximamente'),('realizada', 'realizada'),('realizada-parcial','realizada-parcial'), ('cancelada','cancelada')]
    state=models.CharField(choices = STATE_CHOICES,max_length=50,default='proximamente')
    students = models.ManyToManyField(Student, related_name='class_students',blank=True)
    teachers=models.ManyToManyField(Teacher)  
    num_max_students = models.IntegerField(default=0)
    MODE_CHOICES = [('publico', 'publico'),('privado', 'privado'),('moderado','moderado')]
    mode = models.CharField(choices = MODE_CHOICES,max_length=50,default='moderado')
    label = models.CharField(max_length=100, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def add_students_group(self, group_id):
        group = StudentGroup.objects.get(id=group_id)
        for student in group.students.all():
            if student not in self.students.all():
                self.students.add(student)
                Attendance.objects.create(student=student, class_instance=self)
        

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    PREVIOUS_STATE_CHOICES = [('asistire', 'Asistiré'),('no-asistire', 'no-asistire'),('no-responde', 'No responde')]
    student=models.ForeignKey('Student',on_delete=models.CASCADE, null=True)
    class_instance=models.ForeignKey('ClassInstance',on_delete=models.CASCADE,null=True)
    state=models.BooleanField(default=False)
    user_previous_state=models.CharField(choices = PREVIOUS_STATE_CHOICES,max_length=40,default='no-responde')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class AttendanceHistory(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='history')
    user_previous_state = models.CharField(max_length=40)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
   

class TeacherSubjectRequest(models.Model):
    id=models.AutoField(primary_key=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,null=True)   
    teacher=models.ForeignKey('Teacher',on_delete=models.CASCADE, null=True)     
    STATE_CHOICES = [('pendiente','pendiente'),('aceptado','aceptado'),('rechazado','rechazado')]
    state = models.CharField(max_length=20, default='pendiente')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class StudentSubjectRequest(models.Model):
    id=models.AutoField(primary_key=True)
    subject = models.ForeignKey('Subject',on_delete=models.CASCADE,null=True)  
    student=models.ForeignKey('Student',on_delete=models.CASCADE, null=True)     
    STATE_CHOICES = [('pendiente','pendiente'),('aceptado','aceptado'),('rechazado','rechazado')]
    state = models.CharField(max_length=20, default='pendiente')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class StudentClassRequest(models.Model):
    id=models.AutoField(primary_key=True)
    class_instance = models.ForeignKey('ClassInstance',on_delete=models.CASCADE,null=True)  
    student=models.ForeignKey('Student',on_delete=models.CASCADE, null=True)     
    STATE_CHOICES = [('pendiente','pendiente'),('aceptado','aceptado'),('rechazado','rechazado')]
    state = models.CharField(max_length=20, default='pendiente')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)


class TempFile(models.Model):
    file_data = models.BinaryField()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:        
        if instance.user_type=="profesor":
            Teacher.objects.create(user=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,phone_number=instance.phone_number,document_type=instance.document_type,document_number=instance.document_number)
        if instance.user_type=="alumno":
            Student.objects.create(user=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,phone_number=instance.phone_number)
        if instance.user_type=="apoderado":
            pass


