from django.db.models.aggregates import Count
from courses.models import Cancel, Subject, Course, Class, Customer, CustomerItem, Newsletter
from django.contrib import admin

# Register your models here.

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'subject']
    list_filter = ['subject']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['title', 'schedule', 'startdate', 'course', 'students', 'status']
    list_filter = ['course', 'schedule', 'startdate']
    search_fields = ['title', 'schedule', 'startdate', 'course']
    prepopulated_fields = {'slug': ('title',)}

class CustomerItemAdmin(admin.TabularInline):
    model = CustomerItem
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'fullname', 'phone', 'address']
    search_fields = ['username', 'email', 'phone']

    inlines = [CustomerItemAdmin]

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']
    list_filter = ['created']
    search_fields = ['email']

@admin.register(Cancel)
class CancelAdmin(admin.ModelAdmin):
    list_display = ['customer', 'reg_class', 'created', 'status']
    list_filter = ['status']
    search_fields = ['customer', 'reg_class', 'phone']
