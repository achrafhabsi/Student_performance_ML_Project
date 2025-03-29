from django.contrib import admin
from .models import User, Student, Teacher, Admin, Class , Message

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Class)
admin.site.register(Message)