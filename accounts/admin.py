from django.contrib import admin
from.models import User,Students,Teachers,Courses,Subjects,Attendance
# Register your models here.
class UserDisplay(admin.ModelAdmin):
    list_display = ('id','email','username','firstname','lastname')
admin.site.register(User,UserDisplay)
class StudentsDisplay(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Students,StudentsDisplay)
class TeachersDisplay(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Teachers)
class CoursesDisplay(admin.ModelAdmin):
    list_display = ('course_name','id')
admin.site.register(Courses,CoursesDisplay)
class SubjectsDisplay(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Subjects)
class StudentsAttendance(admin.ModelAdmin):
    list_display = ('id','gender','firstname','lastname')
admin.site.register(Attendance)