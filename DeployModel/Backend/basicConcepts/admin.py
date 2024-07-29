from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.Student)
# admin.site.register(m.AttendanceManager)
admin.site.register(m.Class)