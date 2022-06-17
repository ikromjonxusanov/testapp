from django.contrib import admin

from main.models import Course, Section, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher']


admin.site.register(Section)
admin.site.register(Lesson)
