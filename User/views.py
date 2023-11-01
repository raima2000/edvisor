from django.contrib import messages
from django.contrib.auth import authenticate, decorators, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone

from .forms import *
from .models import *
from Courses.models import ClassAnnouncement
from Home.models import Announcement


# Decorator to check valid user


def CheckValidUser(func):
    def decorate(*args, **kwargs):
        userID = kwargs['id']
        request = args[0]
        if request.user.id == None:
            return HttpResponseRedirect(reverse("login"))
        elif request.user.is_student():
            user = Student.objects.get(id=userID).user_id
        elif request.user.is_lecturer():
            user = Lecturer.objects.get(id=userID).user_id
        else:
            user = User.objects.get(id=userID)
        if request.user == user and request.user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("guest-announcement-page"))

    return decorate


# Create your views here.


def LoginView(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return HttpResponseRedirect(reverse("admin:index"))
            elif user.is_lecturer():
                return HttpResponseRedirect(reverse("lecturer-announcement-page", args=[user.lecturer.id]))
            elif user.is_student():
                return HttpResponseRedirect(reverse("student-announcement-page", args=[user.student.id]))
            else:
                return HttpResponseRedirect(reverse("userinfo", args=[user.id]))
    else:
        form = LoginForm()
    return render(request, "User/login.html", {"form": form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("guest-announcement-page"))


@CheckValidUser
def LecturerAboutView(request, id):
    return render(request, "User/user-about.html",
                  {"userObj": Lecturer.objects.get(id=id).user_id, "page_title": "Personal Information"})


@CheckValidUser
def StudentAboutView(request, id):
    return render(request, "User/user-about.html",
                  {"userObj": Student.objects.get(id=id).user_id, "page_title": "Personal Information"})


def fetch_general_announcements():
    general_announcements = []
    for announcement in Announcement.objects.order_by('-time_modified'):
        is_new = timezone.now() - announcement.time_modified < timezone.timedelta(weeks=1)
        general_announcements.append({"obj": announcement, "is_new": is_new})
    return general_announcements


def fetch_classes_announcements(user):
    classes_announcements = []

    if type(user) is Student:
        classes_queryset = user.class_id
    elif type(user) is Lecturer:
        classes_queryset = user.class_set
    else:
        return classes_announcements

    for announcement in ClassAnnouncement.objects.filter(class_id__in=classes_queryset.all()).order_by(
            "-time_modified"):
        is_new = timezone.now() - announcement.time_modified < timezone.timedelta(weeks=1)
        classes_announcements.append({"obj": announcement, "is_new": is_new})
    return classes_announcements


@CheckValidUser
def StudentUserAnnouncement(request, id):
    student = Student.objects.get(id=id)
    return render(request, "User/user-announcement.html",
                  {"general_announcements": fetch_general_announcements()[:7],
                   "classes_announcements": fetch_classes_announcements(student)[:7]})


@CheckValidUser
def LecturerUserAnnouncement(request, id):
    lecturer = Lecturer.objects.get(id=id)
    return render(request, "User/user-announcement.html",
                  {"general_announcements": fetch_general_announcements()[:7],
                   "classes_announcements": fetch_classes_announcements(lecturer)[:7]})


@CheckValidUser
def StudentGeneralAnnouncementViewAll(request, id):
    return render(request, "User/user-general-announcement-view-all.html",
                  {"general_announcements": fetch_general_announcements()})


@CheckValidUser
def LecturerGeneralAnnouncementViewAll(request, id):
    return render(request, "User/user-general-announcement-view-all.html",
                  {"general_announcements": fetch_general_announcements()})


@CheckValidUser
def StudentClassAnnouncementViewAll(request, id):
    student = Student.objects.get(id=id)
    return render(request, "User/user-class-announcement-view-all.html",
                  {"classes_announcements": fetch_classes_announcements(student)})


@CheckValidUser
def LecturerClassAnnouncementViewAll(request, id):
    lecturer = Lecturer.objects.get(id=id)
    return render(request, "User/user-class-announcement-view-all.html",
                  {"classes_announcements": fetch_classes_announcements(lecturer)})


def fetch_general_announcement(announcement_id):
    general_announcement = Announcement.objects.get(id=announcement_id)
    is_new = timezone.now() - general_announcement.time_modified < timezone.timedelta(weeks=1)
    return {"obj": general_announcement, "is_new": is_new}


@CheckValidUser
def StudentGeneralAnnouncementPage(request, id, announcement_id):
    general_announcement = fetch_general_announcement(announcement_id)
    return render(request, "User/user-general-announcement-page.html", {"general_announcement": general_announcement})


@CheckValidUser
def LecturerGeneralAnnouncementPage(request, id, announcement_id):
    general_announcement = fetch_general_announcement(announcement_id)
    return render(request, "User/user-general-announcement-page.html", {"general_announcement": general_announcement})


def ForgotPasswordView(request):
    if request.method == "POST":
        form = PasswordResetForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if User.objects.filter(email=data["email"]):
                user = User.objects.get(email=data['email'])
                if user.first_name == data['first_name']:
                    user.set_password(data["new_password"])
                    user.save()
                    messages.success(request, 'Form submission successful')
                    return redirect('forgot-password-success')
    else:
        form = PasswordResetForm()
    return render(request, "User/forgot-password.html", {"form": form})


def ForgotPasswordSuccessView(request):
    return render(request, "User/forgot-password-success.html")


def StudentChangePassword(request, id):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('student-change-password-success', request.user.student.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "User/change-password.html", {'form': form, 'student': request.user.student})
    # return render(request, "User/change-password.html", {"student": request.user.student})


def LecturerChangePassword(request, id):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('lecturer-change-password-success', request.user.lecturer.id)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "User/change-password.html", {'form': form, 'lecturer': request.user.lecturer})
    # return render(request, "User/change-password.html", {"lecturer": request.user.lecturer})


@CheckValidUser
def ChangePasswordSuccessView(request, id):
    return render(request, "User/change-password-success.html")
