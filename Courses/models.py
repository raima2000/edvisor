import datetime

import pytz
from django.db import models
from django.db.models import CASCADE, SET_NULL
from User.models import Lecturer

# Create your models here.
class Major(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Course(models.Model):
    major = models.ManyToManyField(Major)
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    day_of_the_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField(auto_now=False, auto_now_add=False)
    duration = models.DurationField()

    @property
    def day_part(self):
        if (self.start_time <= datetime.time(12)):
            return 'Morning'
        else:
            return 'Afternoon'

    def __str__(self):
        return self.day_of_the_week + " " + self.day_part

    class Meta:
        pass
        #ordering = ['day_of_the_week', 'start_time']


class Class(models.Model):
    course = models.ForeignKey(Course, on_delete=CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=SET_NULL, null=True,blank=True)
    start_date = models.DateTimeField(default=datetime.datetime(2021, 9, 6))

    def __str__(self):
        if self.schedule:
            return self.course.name + " - " + str(self.schedule) + " - " + self.lecturer.user_id.full_name + " -  " + self.sem_year
        else:
            return self.course.name + "-" + self.lecturer.user_id.full_name

    @property
    def month(self):
        return int(self.start_date.strftime("%m"))

    @property
    def year(self):
        return int(self.start_date.strftime("%Y"))

    @property
    def sem_year(self):
        year = self.year
        month = self.month
        if month in [9, 10, 11, 12, 1]:
            return "Sem 1 - {}".format(year + 1)
        elif month in [2, 3, 4, 5, 6]:
            return "Sem 2 - {}".format(int(year))

    @property
    def is_displayable(self):
        utc = pytz.UTC
        now = utc.localize(datetime.datetime.now())
        if (now < self.start_date):
            return False
        else:
            return True


class ClassAnnouncement(models.Model):
    class_id = models.ForeignKey(Class, on_delete=CASCADE)
    title = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=False)
    time_modified = models.DateTimeField(auto_now=True)
    content = models.TextField()

    @property
    def is_displayable(self):
        utc = pytz.UTC
        if self.time_created > utc.localize(datetime.datetime.now()):
            return False
        else:
            return True

    def __save__(self):
        self.time_created = datetime.now()

    class Meta:
        ordering = ["time_created", "time_modified"]


class ClassContent(models.Model):
    class_id = models.ForeignKey(Class, on_delete=CASCADE)
    title = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=False)
    time_modified = models.DateTimeField(auto_now=True)
    attached_file = models.FileField(upload_to='', blank=True)
    content = models.TextField(blank=True)

    @property
    def is_displayable(self):
        utc = pytz.UTC
        if self.time_created > utc.localize(datetime.datetime.now()):
            return False
        else:
            return True

    @property
    def file_url(self):
        if self.attached_file and hasattr(self.attached_file, 'url'):
            return self.attached_file.url

    def __save__(self):
        self.time_created = datetime.now()

    class Meta:
        ordering = ["time_created", "time_modified"]


class ClassFeedback(models.Model):
    class_id = models.ForeignKey(Class, on_delete=CASCADE)
    content = models.TextField(max_length=1000, blank=False)
    time_created = models.DateTimeField(auto_now_add=True)

