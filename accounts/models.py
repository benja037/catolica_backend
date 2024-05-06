from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.contrib.auth.models import AbstractUser

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class UserManager(BaseUserManager):
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

class User(AbstractUser):   

    TIPO_GENDER_CHOICES = [('hombre', 'hombre'),('mujer', 'mujer'),]
    objects= UserManager()   
    
    REQUIRED_FIELDS = []   #With this 2 lines make email username
    USUARIO_ALUMNO = 'alumno'
    USUARIO_PROFESOR = 'profesor'
    USUARIO_APODERADO = 'apoderado'
    USUARIO_ADMIN = 'admin'
    TIPO_USUARIO_CHOICES = [(USUARIO_ALUMNO, 'alumno'),(USUARIO_PROFESOR, 'profesor'),(USUARIO_APODERADO, 'apoderado'),(USUARIO_ADMIN,'admin')] 
    email = models.EmailField(unique=True)  
    gender=models.CharField(choices = TIPO_GENDER_CHOICES,max_length=15,null = True)      
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    phone_number = models.CharField(max_length=45,null=True)        
    user_type=models.CharField(choices=TIPO_USUARIO_CHOICES,max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    def __str__(self):
        return self.email
    
    
class Teacher(models.Model):
    id=models.AutoField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    gender=models.CharField(choices = GENDER_CHOICES,max_length=20,null = True)    
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45)
    lastname = models.CharField(max_length=45)
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
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    gender=models.CharField(choices = GENDER_CHOICES,max_length=20,null = True)
    phone_number = models.CharField(max_length=45,null=True)   
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    document_type = models.CharField(max_length=50, null=True)  
    document_number = models.CharField(max_length=50, null=True)  
    def __str__(self):
        return self.firstname + self.lastname
 

class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=50)
    course=models.ForeignKey('Discipline',on_delete=models.SET_NULL, null=True)
    teachers=models.ManyToManyField(Teacher)    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    students = models.ManyToManyField(Student)
    num_max_students = models.IntegerField(default=0)
    public = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)


class StudentGroup(models.Model):
    id=models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student, related_name='groups')    
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
    public = models.BooleanField(default=False)
    label = models.CharField(max_length=100, blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def add_students_group(self, group_id):
        group = StudentGroup.objects.get(id=group_id)
        for student in group.students.all():
            if student not in self.students.all():
                self.students.add(student)

class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    PREVIOUS_STATE_CHOICES = [('asistire', 'Asistiré'),('no-asistire', 'no-asistire'),('no-responde', 'No responde')]
    student=models.ForeignKey('Student',on_delete=models.PROTECT, null=True)
    class_instance=models.ForeignKey('ClassInstance',on_delete=models.CASCADE,null=True)
    state=models.BooleanField(default=False)
    user_previous_state=models.CharField(choices = PREVIOUS_STATE_CHOICES,max_length=40,default='no-responde')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
   

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

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:        
        if instance.user_type=="profesor":
            Teacher.objects.create(user=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,)
        if instance.user_type=="alumno":
            Student.objects.create(user=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,)
        if instance.user_type=="apoderado":
            pass


