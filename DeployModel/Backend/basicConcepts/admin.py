from django.contrib import admin
from . import models as m

# Register your models here.
admin.site.register(m.Student)
admin.site.register(m.Teacher)
admin.site.register(m.Log)
admin.site.register(m.Class)