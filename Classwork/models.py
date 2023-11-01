from django.db import models
import datetime
from django.db.models.deletion import CASCADE

# Create your models here.

class Test(models.Model):
  class_id = models.ForeignKey("Courses.Class",on_delete=CASCADE)
  test_description = models.TextField(null=True,blank=True)
  attached_file = models.FileField(null=True,blank=True,upload_to='tests/')
  test_name = models.CharField(max_length=100)
  publish_time = models.DateTimeField()
  end_time = models.DateTimeField()
  time_modified = models.DateTimeField(auto_now=True)
  available_time_after_deadline = models.DurationField(default=datetime.timedelta(hours=6)) # available for submission after deadline
  is_quiz = models.BooleanField(default=False)
  def __str__(self):
      return self.test_name 

class Question(models.Model):
  test_id = models.ForeignKey(Test,on_delete=CASCADE)
  is_written = models.BooleanField()  # true if written question, false if multiplechoice
  question = models.TextField()
  def __str__(self):
      return self.question

class MultipleChoiceOption(models.Model):
  question = models.ForeignKey(Question,on_delete=CASCADE)
  option = models.CharField(max_length=50)
  is_true = models.BooleanField()
  def __str__(self):
      return self.option
  
class StudentTest(models.Model):
  student_id = models.ForeignKey("User.student",on_delete=CASCADE)
  test_id = models.ForeignKey(Test,on_delete=CASCADE)
  submit_time = models.DateTimeField(auto_now_add=True)
  grade = models.FloatField(blank=True,null=True)
  is_overdue = models.BooleanField(default=False)

class StudentAnswer(models.Model):
  student_test = models.ForeignKey(StudentTest,on_delete=CASCADE)
  question = models.ForeignKey(Question,on_delete=CASCADE)
  written_ans = models.TextField(blank=True,null=True)
  choice_ans = models.ManyToManyField(MultipleChoiceOption,blank=True)
  
class StudentUpload(models.Model):
  studenttest = models.OneToOneField(StudentTest,on_delete=CASCADE)
  attached_file = models.FileField(upload_to='assignments/')
  file_description = models.TextField(null=True,blank=True)
