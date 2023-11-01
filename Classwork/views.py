import os
import zipfile
from datetime import timezone
from uuid import uuid4
from django.http.response import FileResponse, HttpResponse
from django.shortcuts import render
from User.views import CheckValidUser
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from Courses.models import Class
from User.models import Lecturer, Student, User
from django.utils import timezone
from .models import *
from .forms import *
from django.conf import Settings, settings
# Create your views here.

def CheckValidUser(func):
    def decorate(*args, **kwargs):
        userID = kwargs['id']
        classID=kwargs['class_id']
        request = args[0]
        if request.user.id==None:
            return HttpResponseRedirect(reverse("login"))
        elif request.user.is_student():
            return HttpResponseRedirect(reverse('student-class-announcement-page',args=[userID,classID]))
        elif request.user.is_lecturer():
            user = Lecturer.objects.get(id=userID).user_id
        else:
            user = User.objects.get(id=userID)
        if request.user == user and request.user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("guest-announcement-page"))
    return decorate
  
def DownloadTestFile(request, id, class_id, test_id):
    test = Test.objects.get(id=test_id)
    # path = test.attached_file.url
    # file_path = str(settings.BASE_DIR).replace("\\","/") + path
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as fh:
    #         response = HttpResponse(fh.read(), content_type="application/pdf")
    #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #         return response
    # raise Http404
    file = test.attached_file.path
    response = FileResponse(open(file,'rb'))
    if response:
      return response
    else:
      return Http404

def DownloadStudentFile(request,id,class_id, studenttest_id):
    test = StudentTest.objects.get(id= studenttest_id).studentupload
    # path = test.attached_file.url
    # file_path = str(settings.BASE_DIR).replace("\\","/") + path
    # if os.path.exists(file_path):
    #     with open(file_path, 'rb') as fh:
    #         response = HttpResponse(fh.read(), content_type="application/pdf")
    #         response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
    #         return response
    # raise Http404
    file = test.attached_file.path
    response = FileResponse(open(file,'rb'))
    if response:
      return response
    else:
      return Http404  
@CheckValidUser
def CreateClassworkView(request, id, class_id):
  context={'id':id,'class_id':class_id,"new":True}
  if request.method == 'POST':
    form = TestForm(request.POST,request.FILES)
    if(form.is_valid()):
      t = form.save(commit=False)
      t.class_id = Class.objects.get(id=class_id)
      t.save()
      return HttpResponseRedirect(reverse("lecturer-class-assignment-page",args=[id,class_id]))
  else:
    form = TestForm()
  context['form'] = form
  context['lecturer_class'] = Class.objects.get(id=class_id)
  return render(request, "Classwork/create-classwork.html",context)

@CheckValidUser
def ChangeTestInformation(request, id, class_id, test_id):
  test = Test.objects.get(id=test_id)

  if request.method == 'POST':
    form = TestForm(request.POST,request.FILES, instance=test)
    if(form.is_valid()):
      form.save()
      test.save()
      return HttpResponseRedirect(reverse("lecturer-class-assignment-page",args=[id,class_id]))
  else:  
    form = TestForm(instance=test)
    context= {"id":id,"class_id":class_id,"test_id":test_id,"form":form,"test":test}
    return render(request, "Classwork/create-classwork.html",context)


@CheckValidUser
def ClassworkView(request, id, class_id):
  lecturer = Lecturer.objects.get(id=id)
  c = Class.objects.get(id=class_id)
  context={'id':id,'class_id':class_id}
  tests = c.test_set.all()
  context['tests']=tests
  return render(request,'Classwork/view-classwork.html', context)

@CheckValidUser
def EditClassworkView(request, id, class_id , test_id):
  lecturer = Lecturer.objects.get(id=id)
  class_id = Class.objects.get(id=class_id)
  test = Test.objects.get(id=test_id)
  if request.method == "POST":
    print(request.POST)
  context = {'id':id,'class_id':class_id.id,'test':test,'test_id':test_id}
  return render(request,'Classwork/edit-classwork.html',context)

def UploadAssignmentview(request,id,class_id,test_id):
  studenttest= None
  done=False
  grade = None
  if request.user.is_lecturer():
    return HttpResponseRedirect(reverse("student-class-assignment-page",args=[id,class_id]),args=[id,class_id])
  t = Test.objects.get(id=test_id)
  if t.is_quiz:
    return HttpResponseRedirect(reverse("student-class-assignment-page",args=[id,class_id]),args=[id,class_id])
  now = timezone.localtime()+timezone.timedelta(hours=7)
  if not t.publish_time <= now:
    HttpResponseRedirect(reverse('student-class-announcement-page',args=[id,class_id]))
  if t.studenttest_set.filter(student_id=id,test_id=test_id).exists():
    studenttest = t.studenttest_set.get(student_id=id,test_id=test_id)
    done = True
    grade = studenttest.grade
  if request.method == "POST":
    isoverdue = t.end_time <= now+ t.available_time_after_deadline
    test = StudentTest(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id),is_overdue=isoverdue)
    test.save()
    form = StudentUploadForm(request.POST,request.FILES)
    form.studenttest = StudentTest.objects.get(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id))
    if form.is_valid():
      f=form.save(commit=False)
      f.studenttest = StudentTest.objects.get(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id))
      f.save()
    return HttpResponseRedirect(reverse('upload-assignment',args=[id,class_id,test_id]))
  else:
    form = StudentUploadForm()
    if StudentTest.objects.filter(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id)).exists():
      studenttest=StudentTest.objects.get(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id))
    context={'test':Test.objects.get(id=test_id), "done":done, "id":id,"class_id":class_id,"grade":grade,"form":form,"studenttest":studenttest,"student_class":Class.objects.get(id=class_id)}
    return render(request,"Classwork/upload-assignment.html",context)

def DoTestView(request,id,class_id,test_id):
  done=False
  grade = None
  a=None
  if request.user.is_lecturer():
    return HttpResponseRedirect(reverse("student-class-assignment-page",args=[id,class_id]),args=[id,class_id])
  t = Test.objects.get(id=test_id)
  now = timezone.localtime()+timezone.timedelta(hours=7)
  if not t.publish_time <= now:
    HttpResponseRedirect(reverse('student-class-assignment-page',args=[id,class_id]))
  if t.studenttest_set.filter(student_id=id,test_id=test_id).exists():
    a = t.studenttest_set.get(student_id=id,test_id=test_id)
    done = True
    grade = a.grade
  if request.method == 'POST':
    # print(dict(request.POST.lists()))
    isoverdue = t.end_time <= now+ t.available_time_after_deadline
    test = StudentTest(student_id=Student.objects.get(id=id),test_id=Test.objects.get(id=test_id),is_overdue=isoverdue)
    test.save()
    for question, answer in dict(request.POST.lists()).items():
      if question != 'csrfmiddlewaretoken':
        q = Question.objects.get(id=int(question))
        a = StudentAnswer(student_test=test,question=q)
        a.save()
        if q.is_written:
          a.written_ans=answer[0]
        else:
          for mco in answer:
            a.choice_ans.add(MultipleChoiceOption.objects.get(id=int(mco)))
        a.save()
    return HttpResponseRedirect(reverse('do-test',args=[id,class_id,test_id]))
  context={'test':Test.objects.get(id=test_id), "done":done, "id":id,"class_id":class_id,"grade":grade,"student_class":Class.objects.get(id=class_id)}
  return render(request,"Classwork/do-test.html",context)

@CheckValidUser
def ViewStudentTest(request,id,class_id,studenttest_id):
  st = StudentTest.objects.get(id=studenttest_id)
  g = None
  if st.grade!=None:
    g = st.grade
  if request.method == "POST":
    grade = float(request.POST['grade'])
    if grade >= 0:
      st.grade = grade
      st.save()
    return HttpResponseRedirect(reverse("submitted-view",args=[id,class_id,st.test_id.id]))
  right_ans=0
  for ans in st.studentanswer_set.all():
    if not ans.question.is_written:
        q = ans.question.multiplechoiceoption_set.all()
        right = [answer for answer in q if answer.is_true]
        if(set(ans.choice_ans.all())==set(right)):
          right_ans+=1
  context = {"class_id":class_id, "id":id,"test":st,"right":right_ans,"grade":g,"lecturer_class":Class.objects.get(id=class_id)}
  return render(request,"Classwork/view-student-test.html",context)

@CheckValidUser
def written_question_form(request,id,class_id,test_id):
  form = MultipleChoiceQuestionForm()
  if request.method == 'POST':
    q = Question(question=request.POST['question'],is_written=True,test_id=Test.objects.get(id=test_id))
    q.save()
    return HttpResponseRedirect(reverse("edit-classwork-view",args=[id,class_id,test_id]))
  context={'form':form}
  return render(request,"Classwork/partials/partial-written-form.html",context)

@CheckValidUser
def multiplechoice_form(request,id,class_id,test_id):
  error=""
  form = MultipleChoiceQuestionForm()
  qid=str(uuid4())[:5]
  form.fields['q.'+qid]=form.fields['question']
  del form.fields['question']
  context = {'form':form,"id":id,"class_id":class_id,"qid":qid}
  if request.method == 'POST':
    questions,options,correctoptions = parseMultipleChoice(request)
    for k,v in questions.items():
      q = Question(question=v,is_written=False,test_id=Test.objects.get(id=test_id))
      q.save()
      for m,n in options.items():
        if m in correctoptions.keys():
          o = MultipleChoiceOption(option=n,is_true=True,question=q)
        else:
          o=MultipleChoiceOption(option=n,is_true=False,question=q)
        o.save()
    return HttpResponseRedirect(reverse("edit-classwork-view",args=[id,class_id,test_id]))
  return render(request,"Classwork/partials/partial-multiplechoice-form.html",context)


def parseMultipleChoice(request):
  questions={}
  options={}
  correctoptions={}
  for i in request.POST.keys():
    if 'q.' in i:
      questions[i]=request.POST[i]
    if 'o.' in i:
      options={request.POST.getlist('optionid')[k]:request.POST.getlist(i)[k] for k in range(len(request.POST.getlist(i)))}
  for k,v in options.items():
    if "i."+k in request.POST.keys():
      correctoptions[k]=v
  return (questions,options,correctoptions)

@CheckValidUser
def mco_form(request,id,class_id,qid):
  oid = str(uuid4())[:5]
  form = MultipleChoiceOptionForm(initial={'optionid':oid})
  form.fields['o.'+qid]=form.fields['option']
  del form.fields['option']
  form.fields['i.'+oid]=form.fields['is_true']
  del form.fields['is_true']
  context = {'form': form,"id":id,"class_id":class_id}
  return render(request,"Classwork/partials/partial-mco-form.html",context)

@CheckValidUser
def DeleteTest(request,id,class_id,test_id):
  test = Test.objects.get(id=test_id)
  context = {'id':id,'class_id':class_id,'test_id':test_id,'test':test,"lecturer_class":Class.objects.get(id=class_id)}
  if request.method == "POST":
    test.delete()
    return HttpResponseRedirect(reverse("lecturer-class-assignment-page",args=[id,class_id]))
  return render(request,"Classwork/delete-classwork.html",context)

@CheckValidUser
def DeleteQuestion(request,id,class_id,test_id,qid):
  q = Question.objects.get(id=qid)
  q.delete()
  return HttpResponseRedirect(reverse("edit-classwork-view",args=[id,class_id,test_id]))

@CheckValidUser
def UpdateQuestion(request,id,class_id,test_id,qid):
  q=Question.objects.get(id=qid)
  context={'id':id,'class_id':class_id,'test_id':test_id,'question':q}
  if request.method == "POST":
    if q.is_written:
      for option in q.multiplechoiceoption_set.all():
        option.option = request.POST.getlist(str(option.id))[0]
        if len(request.POST.getlist(str(option.id))) == 2:
          option.is_true=True
        else:
          option.is_true=False
        option.save()
    return HttpResponseRedirect(reverse("edit-classwork-view",args=[id,class_id,test_id]))
  return render(request,"Classwork/update-question.html",context)

@CheckValidUser
def SubmittedListView(request, id, class_id, test_id):
  submitted = Test.objects.get(id=test_id).studenttest_set.all()
  times = [t.submit_time + datetime.timedelta(hours=7) for t in submitted]
  list = zip(submitted,times)
  context={'id':id,'class_id':class_id,'test_id':test_id,'submitted':list,"lecturer_class":Class.objects.get(id=class_id)}
  return render(request,"Classwork/submitted-list.html",context)