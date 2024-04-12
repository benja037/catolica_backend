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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    USUARIO_ALUMNO = 'alumno'
    USUARIO_PROFESOR = 'profesor'
    USUARIO_APODERADO = 'apoderado'
    TIPO_USUARIO_CHOICES = [(USUARIO_ALUMNO, 'alumno'),      (USUARIO_PROFESOR, 'profesor'),(USUARIO_APODERADO, 'apoderado'),]    

    email = models.CharField(max_length=80,unique=True)
    username=models.CharField(max_length=45)
    gender=models.CharField(choices = TIPO_GENDER_CHOICES,max_length=255,null = True)      
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    phone_number = models.CharField(max_length=45,null=True)        
    user_type=models.CharField(choices=TIPO_USUARIO_CHOICES,max_length=10)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.username
    
    
class Teachers(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    TIPO_GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    gender=models.CharField(choices = TIPO_GENDER_CHOICES,max_length=255,null = True)    
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    def __str__(self):
        return self.firstname + self.lastname
    

class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.course_name


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    TIPO_GENDER_CHOICES = [
        ('Hombre', 'Hombre'),
        ('Mujer', 'Mujer'),
    ]
    gender=models.CharField(choices = TIPO_GENDER_CHOICES,max_length=255,null = True)        
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    #subjects = models.ManyToManyField(Subjects)
 

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey('Courses',on_delete=models.SET_NULL, null=True)
    staff_id=models.ForeignKey('Teachers',on_delete=models.SET_NULL, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    alumnos = models.ManyToManyField(Students)
    finished = models.BooleanField(default=False)

class Horario(models.Model):
    DAYS_CHOICES = [('lunes', 'lunes'),('martes', 'martes'),('miercoles','miercoles'), ('jueves','jueves'), ('viernes','viernes'), ('sabado','sabado'), ('domingo','domingo')]
    subject_id=models.ForeignKey('Subjects',on_delete=models.CASCADE,null=True)
    day_of_week = models.CharField(choices = DAYS_CHOICES,max_length=15,default=None)  
    time= models.TimeField()
    alumnos_horario = models.ManyToManyField(Students,blank=True)


class Clase(models.Model):
    id=models.AutoField(primary_key=True)
    date_and_hour= models.DateTimeField()
    horario_id=models.ForeignKey('Horario',on_delete=models.PROTECT,null=True)
    ESTADOS_CHOICES = [('proximamente', 'proximamente'),('realizada', 'realizada'),('realizada-parcial','realizada-parcial'), ('cancelada','cancelada')]
    estado=models.CharField(choices = ESTADOS_CHOICES,max_length=255,default='proximamente')
    

class Attendance(models.Model):

    ESTADO_PREVIO_CHOICES = [('asistire', 'Asistiré'),('no-asistire', 'no-asistire'),('no-responde', 'No responde')
    ]
            
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey('Students',on_delete=models.PROTECT, null=True)
    clase_id=models.ForeignKey('Clase',on_delete=models.CASCADE,null=True)       
    estado=models.BooleanField(default=False)
    user_estado_previo=models.CharField(choices = ESTADO_PREVIO_CHOICES,max_length=255,default='no-responde')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
   

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:        
        if instance.user_type=="profesor":
            Teachers.objects.create(admin=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,)
        if instance.user_type=="alumno":
            Students.objects.create(admin=instance,date_of_birth=instance.date_of_birth,firstname=instance.firstname,lastname=instance.lastname,gender=instance.gender,)
        if instance.user_type=="apoderado":
            pass


"""
gender=models.CharField(max_length=255)    
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    phone_number = models.CharField(max_length=45,null=True)
"""
""" @receiver(post_save,sender=User)
def save_user_profile(sender,instance,**kwargs):
    
    if instance.user_type=="profesor":
        Teachers.save()
    if instance.user_type=="alumno":
        Students.save() 
 """
""" class LeaveReportStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Students,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_message = models.TextField()
    leave_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationTeacher(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
 """

