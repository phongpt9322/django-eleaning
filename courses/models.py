from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.contrib.auth.hashers import make_password
# Create your models here.

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    subject = models.ForeignKey(Subject,
            related_name='courses',
            on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="courses",
                              default="courses/no-image.png")
    overview = RichTextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    schedule = models.DateField(null=True)
    duration = models.IntegerField(null=True)
    tuitionfee = models.FloatField(default=0.0)
    tuitionfee_ori = models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Class(models.Model):
    course = models.ForeignKey(Course, related_name="classes", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    schedule = models.DateField(null=True)
    startdate = models.CharField(max_length=100)
    numofsession = models.IntegerField(null=True)
    students = models.IntegerField(null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    fullname = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=250, unique=False)
    
    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

class CustomerItem(models.Model):
    customer = models.ForeignKey(Customer, related_name="customers", on_delete=models.CASCADE)
    reg_class = models.ForeignKey(Class, related_name="reg_classes", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

class Cancel(models.Model):
    customer = models.ForeignKey(Customer, related_name="cancel_customer", on_delete=models.CASCADE)
    reg_class = models.ForeignKey(Class, related_name="cancel_class", on_delete=models.CASCADE)
    reason = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.reg_class)

class Newsletter(models.Model):
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email