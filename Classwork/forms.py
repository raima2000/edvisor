from django import forms
from django.forms import widgets
from .models import *

class TestForm(forms.ModelForm):
  # publish_time = forms.DateTimeField(label='Publish time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
  # end_time = forms.DateTimeField(label='End time', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
  
  class Meta:
    model = Test
    fields = [
      "test_name",
      "test_description",
      "attached_file",
      "publish_time",
      "end_time",
      "available_time_after_deadline",
      "is_quiz"
      ]
    # widgets={
    #   "publish_time":widgets.DateTimeInput(attrs={'type':'datetime-local'}),
    #   "end_time":forms.DateTimeInput(attrs={'type':'datetime-local'}),
    # }
    widgets={
      "publish_time":forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
      "end_time":forms.DateTimeInput(format='%Y-%m-%d %H:%M:%S', attrs={'class':'datetimefield'}),
      "attached_file":forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    }

class WrittenQuestionForm(forms.Form):
  question = forms.CharField(label='Question')

class MultipleChoiceQuestionForm(forms.Form):
  question = forms.CharField(label='Question')
  
class StudentUploadForm(forms.ModelForm):
  class Meta:
    model = StudentUpload
    fields = ["attached_file","file_description"]
    widgets={
      "file": forms.ClearableFileInput(attrs={'allow_multiple_selected': True}),
    }

class MultipleChoiceOptionForm(forms.Form):
  optionid = forms.CharField(widget=forms.HiddenInput,required=False)
  option = forms.CharField(label='Option')
  is_true = forms.BooleanField(label = "Is true",required=False,initial=False)

# class WrittenQuestionForm(forms.ModelForm):
#   class Meta:
#     model = Question
#     fields = ["question"]

# class MultipleChoiceQuestionForm(forms.ModelForm):
#   class Meta:
#     model = Question
#     fields = ["question"]

# class MultipleChoiceOptionForm(forms.ModelForm):
#   class Meta:
#     model = MultipleChoiceOption
#     fields = ["is_true","option"]