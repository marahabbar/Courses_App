from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
# Create your models here.

# class User(AbstractBaseUser):
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_teacher = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_student = models.BooleanField(default=False)
class User(AbstractUser):
    username = models.CharField(max_length = 50)
    # first_name = models.CharField(max_length = 180)
    # last_name = models.CharField(max_length = 180)
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    # username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    # def __str__(self):
    #     return "{}".format(self.email)  

class University(models.Model):
    name = models.CharField(max_length = 180)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length = 180)
    brief= models.CharField(max_length = 255)

    def __str__(self):
        return self.name

class University_Faculty(models.Model):
    faculty=models.ForeignKey(Faculty, on_delete = models.CASCADE)
    university=models.ForeignKey(University, on_delete = models.CASCADE)

    def __str__(self):
        return self.faculty

class Year(models.Model):
    name = models.CharField(max_length = 180)

    def __str__(self):
        return self.name
def Course_Files(instance, filename):
    return '/'.join( ['uploads','courses_images', str(instance.id), filename] )

class Course(models.Model):
    name = models.CharField(max_length = 180)
    description= models.CharField(max_length = 255)
    price= models.FloatField(null=True)
    Duration=models.DurationField(null=True)
    Image = models.ImageField(upload_to=Course_Files,null=True)



    # def __str__(self):
    #     return self.name

class Year_Course(models.Model):
    year=models.ForeignKey(Year, on_delete = models.CASCADE)
    course=models.ForeignKey(Course, on_delete = models.CASCADE)

    def __str__(self):
        return self.faculty


class section(models.Model):
    name = models.CharField(max_length = 180)
    description= models.CharField(max_length = 255)
    course=models.ForeignKey(Course, on_delete = models.CASCADE)
    price= models.FloatField(null=True)


    def __str__(self):
        return self.name

class Instructor(models.Model):
    first_name = models.CharField(max_length = 180)
    last_name = models.CharField(max_length = 180)
    email = models.EmailField()
    brief= models.CharField(max_length = 255)
    phone= PhoneNumberField(unique = True, null = False, blank = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name

class Instructor_Course(models.Model):
    course=models.ForeignKey(Course, on_delete = models.CASCADE)
    instructor=models.ForeignKey(Instructor, on_delete = models.CASCADE)

    def __str__(self):
        return self.course


class Quiz(models.Model):
    title = models.CharField(max_length = 180)
    section=models.ForeignKey(section, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    question= models.CharField(max_length = 255)
    first_choice = models.CharField(max_length = 180)
    second_choice = models.CharField(max_length = 180)
    third_choice = models.CharField(max_length = 180)
    forth_choice = models.CharField(max_length = 180)
    right_choice = models.SmallIntegerField()
    quiz=models.ForeignKey(Quiz, on_delete = models.CASCADE)
    def __str__(self):
        return self.question

class Video(models.Model):
    title = models.CharField(max_length = 180)
    url = models.URLField()
    section=models.ForeignKey(section, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class Assessed_Reading(models.Model):
    title = models.CharField(max_length = 180)
    content = models.TextField()
    section=models.ForeignKey(section, on_delete = models.CASCADE)

    def __str__(self):
        return self.title   


class Student(models.Model):
    first_name = models.CharField(max_length = 180)
    last_name = models.CharField(max_length = 180)
    email = models.EmailField()
    phone= PhoneNumberField(unique = True, null = False, blank = False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.first_name


class studied(models.Model):
    assessed_reading = models.ForeignKey(Assessed_Reading, on_delete = models.CASCADE)
    video =models.ForeignKey(Video, on_delete = models.CASCADE)
    student=models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

class Enrolled_section(models.Model):
    enrollment_date = models.DateField()
    expiry_date = models.DateField()
    section =models.ForeignKey(section, on_delete = models.CASCADE)
    student=models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return self.enrollment_date        

class Answered_Question(models.Model):
    answer = models.SmallIntegerField()
    question =models.ForeignKey(Question, on_delete = models.CASCADE)
    student=models.ForeignKey(Student, on_delete = models.CASCADE)

    def __str__(self):
        return self.answer 