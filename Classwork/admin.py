from django.contrib import admin
from .models import *
# Register your models here.

class QuestionInline(admin.TabularInline):
  model = Question
class OptionInline(admin.TabularInline):
  model = MultipleChoiceOption

class TestAdmin(admin.ModelAdmin):
  inlines=[QuestionInline]

class QuestionAdmin(admin.ModelAdmin):
  inlines=[OptionInline]

admin.site.register(Test,TestAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(StudentTest)
admin.site.register(StudentAnswer)