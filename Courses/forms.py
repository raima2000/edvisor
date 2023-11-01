import pytz

from Courses.models import ClassAnnouncement, ClassContent, Class, ClassFeedback
from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta

utc = pytz.UTC

class UploadClassAnnouncementForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Announcement Title'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(
        attrs={'placeholder': 'Announcement Content'}))
    time_created = forms.DateTimeField(label='Time displayed', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean_time_created(self):
        time_created = self.cleaned_data['time_created']
        if time_created < utc.localize(datetime.now()):
            raise forms.ValidationError("Time displayed must not be in the past.")
        elif time_created > utc.localize(datetime.now() + timedelta(days=7)):
            raise forms.ValidationError("Only choose display time within this week.")
        return time_created

    class Meta:
        model = ClassAnnouncement
        fields = [
            'title',
            'content',
            'time_created'
        ]


class UploadClassContentForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Content Title'}))
    content = forms.CharField(label='Description', widget=forms.Textarea(
        attrs={'placeholder': 'Content Description'}))
    time_created = forms.DateTimeField(label='Time displayed', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean_time_created(self):
        time_created = self.cleaned_data['time_created']
        if time_created < utc.localize(datetime.now()):
            raise forms.ValidationError("Time displayed must not be in the past.")
        elif time_created > utc.localize(datetime.now() + timedelta(days=7)):
            raise forms.ValidationError("Only choose display time within this week.")
        return time_created

    class Meta:
        model = ClassContent
        fields = [
            'attached_file',
            'title',
            'content',
            'time_created'
        ]


class ClassRegistrationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices')
        super(ClassRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['selection'] = forms.MultipleChoiceField(choices=choices,widget=forms.CheckboxSelectMultiple)

    def clean_selection(self):
        selection = self.cleaned_data['selection']
        duplicates = any(selection.choice_label.count(i) for i in selection.choice_label)
        if duplicates > 0:
            raise forms.ValidationError('Dup')
        return selection

    class Meta:
        model = Class


class EditClassRegistrationForm(forms.Form):
    selection = forms.BooleanField(widget=forms.CheckboxSelectMultiple)


class EditClassAnnouncementForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Announcement Title'}))
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder': 'Announcement Content'}))

    class Meta:
        model = ClassAnnouncement
        fields = ['title', 'content']


class EditClassContentForm(forms.ModelForm):
    title = forms.CharField(label='Title', widget=forms.TextInput(attrs={'placeholder': 'Content Title'}))
    content = forms.CharField(label='Description', widget=forms.Textarea(attrs={'placeholder': 'Content Description'}))
    attached_file = forms.FileField(label='File', required=False, widget=forms.ClearableFileInput(attrs={'allow_multiple_selected':True}))
    class Meta:
        model = ClassContent
        fields = ['attached_file', 'title', 'content']


class UploadClassFeedbackForm(forms.ModelForm):
    content = forms.CharField(label='Content', widget=forms.Textarea(attrs={'placeholder': '...'}))

    class Meta:
        model = ClassFeedback
        fields = ['content']