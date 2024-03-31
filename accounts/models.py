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
    email = models.CharField(max_length=80,unique=True)
    username=models.CharField(max_length=45)
    date_of_birth=models.DateField(null=True)
    firstname = models.CharField(max_length=45,null=True)
    lastname = models.CharField(max_length=45,null=True)
    objects= UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    USUARIO_ALUMNO = 'alumno'
    USUARIO_PROFESOR = 'profesor'

    TIPO_USUARIO_CHOICES = [
        (USUARIO_ALUMNO, 'Alumno'),
        (USUARIO_PROFESOR, 'Profesor'),
    ]

    
    user_type=models.CharField(choices=TIPO_USUARIO_CHOICES,max_length=10)
 
    def __str__(self):
        return self.username
    
    
class Teachers(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)


class Students(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)    
    address=models.TextField()        
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

class Subjects(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey('Courses',on_delete=models.CASCADE)
    staff_id=models.ForeignKey('Teachers',on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    alumnos = models.ManyToManyField(Students)


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey('Students',on_delete=models.CASCADE, null=True)
    subject_id=models.ForeignKey('Subjects',on_delete=models.CASCADE)
    dateandhour = models.DateTimeField(null = True)
    
    estado=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
   

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:        
        if instance.user_type=="Profesor":
            Teachers.objects.create(admin=instance,address="")
        if instance.user_type=="Alumno":
            Students.objects.create(admin=instance,address="",gender="")

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

