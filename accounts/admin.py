from django.contrib import admin
from .models import ClassInstance, StudentGroup, CustomUser,Student, StudentSubjectRequest,Teacher,Discipline,Subject,Attendance

from django.contrib import admin

class CustomUserDisplay(admin.ModelAdmin):
    list_display = ('id', 'email', 'is_staff')
admin.site.register(CustomUser,CustomUserDisplay)
class StudentDisplay(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Student,StudentDisplay)
class TeacherDisplay(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Teacher,TeacherDisplay)
class DisciplineDisplay(admin.ModelAdmin):
    list_display = ('id','discipline_name')
admin.site.register(Discipline,DisciplineDisplay)
class SubjectDisplay(admin.ModelAdmin):
    list_display = ('id','subject_name') 
admin.site.register(Subject,SubjectDisplay)
class AttendanceDisplay(admin.ModelAdmin):
    list_display = ('id','student','class_instance','updated_at') 
admin.site.register(Attendance,AttendanceDisplay)
class StudentGroupDisplay(admin.ModelAdmin):
    list_display = ('id','name')
admin.site.register(StudentGroup,StudentGroupDisplay)

class ClassInstanceDisplay(admin.ModelAdmin):
    list_display = ('id','date','time_start','time_end','state')
admin.site.register(ClassInstance,ClassInstanceDisplay)

class StudentSubjectRequestDisplay(admin.ModelAdmin):
    list_display = ('id','subject','student','state')
admin.site.register(StudentSubjectRequest,StudentSubjectRequestDisplay)