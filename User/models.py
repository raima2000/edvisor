
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.deletion import CASCADE, SET_NULL
from django.db import models

# Create your models here.

class MyUserManager(BaseUserManager):
    def create_user(self, email, password, **other):
        """
        Creates and saves a User 
        """
        user = self.model(
            email=self.normalize_email(email),
            **other
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **other):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password,
            **other
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    objects = MyUserManager()
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=12, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    type= [
        ("Student","student"),
        ("Lecturer","lecturer")
    ]
    user_type = models.CharField(max_length=10,choices=type,null=True,blank=True)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self, app_label: str) -> bool:
        return True
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs) 
        if self.user_type:
            if self.user_type.lower() == "student":
                if Lecturer.objects.filter(user_id = self):
                    Lecturer.objects.get(user_id=self).delete()
                if not Student.objects.filter(user_id=self):
                    Student.objects.create(user_id = self)
            elif self.user_type.lower() == "lecturer":
                if Student.objects.filter(user_id = self):
                    Student.objects.get(user_id=self).delete()
                if not Lecturer.objects.filter(user_id=self):
                    Lecturer.objects.create(user_id = self)
    def is_student(self):
        return hasattr(self,'student')
    def is_lecturer(self):
        return hasattr(self,'lecturer')

    @property
    def full_name(self):
        return self.last_name + " " + self.middle_name + " " + self.first_name


class Student(models.Model):
    user_id = models.OneToOneField(User,on_delete=CASCADE)
    major_id = models.ForeignKey("Courses.Major",on_delete=SET_NULL,null=True)
    class_id = models.ManyToManyField("Courses.Class")

    def __str__(self):
        return User.objects.get(pk=self.user_id.pk).email

    def save(self,*args,**kwargs):
        created = not self.pk
        self.user_id.user_type= "Student"
        if Lecturer.objects.filter(user_id=self.user_id):
            Lecturer.objects.get(user_id=self.user_id).delete()
        super().save(*args,**kwargs)


class Lecturer(models.Model):
    user_id= models.OneToOneField(User,on_delete=CASCADE)

    def __str__(self):
        return User.objects.get(pk=self.user_id.pk).email

    def save(self,*args,**kwargs):
        created = not self.pk
        self.user_id.user_type= "Lecturer"
        if Student.objects.filter(user_id=self.user_id):
            Student.objects.get(user_id=self.user_id).delete()
        super().save(*args,**kwargs)    
