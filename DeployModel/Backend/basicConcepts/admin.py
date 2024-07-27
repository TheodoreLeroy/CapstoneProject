from django.contrib import admin
import models as m

# Register your models here.
admin.site.register(m.Student, m.AttendanceManager, m.Class)