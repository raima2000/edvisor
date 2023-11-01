from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone

from User.models import User
from User.views import CheckValidUser, fetch_general_announcements, fetch_general_announcement
from .models import Announcement


# Decorator to redirect authenticated users
def redirect_auth_user(func):
    def decorate(*args, **kwargs):
        request = args[0]
        if request.user.is_authenticated:
            user = User.objects.get(id=request.user.id)
            if user.is_student():
                return HttpResponseRedirect(reverse("student-announcement-page", args=[user.student.id]))
            if user.is_lecturer():
                return HttpResponseRedirect(reverse("lecturer-announcement-page", args=[user.lecturer.id]))
        else:
            return func(*args, **kwargs)
    return decorate


# Create your views here.

@redirect_auth_user
def GuestAnnouncement(request):
    return render(request, "User/user-announcement.html",
                  {"general_announcements": fetch_general_announcements()[:7]})


@redirect_auth_user
def GuestAnnouncementAll(request):
    general_announcements = []
    for i in Announcement.objects.all().order_by('-time_created'):
        general_announcements.append(i)
    return render(request, "User/user-general-announcement-view-all.html",
                  {"general_announcements": fetch_general_announcements()})


def fetch_searched_general_announcements(title__icontains):
    general_announcements = []
    for announcement in Announcement.objects.filter(title__icontains=title__icontains).order_by('-time_modified'):
        is_new = timezone.now() - announcement.time_modified < timezone.timedelta(weeks=1)
        general_announcements.append({"obj": announcement, "is_new": is_new})
    return general_announcements


def GuestAnnouncementSearch(request): # new
        query = request.GET.get('search')
        if query is None:
            context = fetch_general_announcements()
            return render(request, "User/user-general-announcement-view-all.html", context)
        else:
            general_announcement = fetch_searched_general_announcements(title__icontains=query)
            context = {"general_announcements": general_announcement}
            return render(request, "User/user-general-announcement-view-all.html", context)


@redirect_auth_user
def GuestAnnouncementPage(request, announcement_id):
    general_announcement = fetch_general_announcement(announcement_id)
    return render(request, "User/user-general-announcement-page.html", {"general_announcement": general_announcement})


def About(request):
    return render(request, "Home/about.html")


def Talents(request):
    return render(request, "Home/talents.html")


def Contact(request):
    return render(request, "Home/contact.html")
