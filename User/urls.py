from django.urls import path, include
from . import views
from Courses import views as coursesViews

urlpatterns = [
    path('login/',views.LoginView,name="login"),
    path('logout/',views.LogoutView,name="logout"),
    path('forgot/', views.ForgotPasswordView, name="forgot-password"),
    path('forgot/success/', views.ForgotPasswordSuccessView, name="forgot-password-success"),
    path('lecturer/<int:id>/about/', views.LecturerAboutView, name="lecturer-about"),
    path('lecturer/<int:id>/change-password/', views.LecturerChangePassword, name="lecturer-change-password"),
    path('lecturer/<int:id>/change-password/success', views.ChangePasswordSuccessView, name="lecturer-change-password-success"),
    path('lecturer/<int:id>/announcement/', views.LecturerUserAnnouncement, name="lecturer-announcement-page"),
    path('lecturer/<int:id>/announcement/general/all', views.LecturerGeneralAnnouncementViewAll, name="lecturer-general-announcement-all"),
    path('lecturer/<int:id>/announcement/class/all', views.LecturerClassAnnouncementViewAll, name="lecturer-class-announcement-all"),
    path('lecturer/<int:id>/announcement/<int:announcement_id>', views.LecturerGeneralAnnouncementPage, name="lecturer-general-announcement-page"),
    path('lecturer/<int:id>/active-classes/', coursesViews.ActiveLecturerClasses, name="active-lecturer-classes-page"),
    path('lecturer/<int:id>/calendar/', coursesViews.LecturerSchedule, name="lecturer-schedule-page"),
    path('student/<int:id>/about/', views.StudentAboutView, name="student-about"),
    path('student/<int:id>/change-password/', views.StudentChangePassword, name="student-change-password"),
    path('student/<int:id>/change-password/success', views.ChangePasswordSuccessView, name="student-change-password-success"),
    path('student/<int:id>/announcement/', views.StudentUserAnnouncement, name="student-announcement-page"),
    path('student/<int:id>/announcement/general/all', views.StudentGeneralAnnouncementViewAll, name="student-general-announcement-all"),
    path('student/<int:id>/announcement/class/all', views.StudentClassAnnouncementViewAll, name="student-class-announcement-all"),
    path('student/<int:id>/announcement/<int:announcement_id>', views.StudentGeneralAnnouncementPage, name="student-general-announcement-page"),
    path('student/<int:id>/active-classes/', coursesViews.ActiveStudentClasses, name="active-student-classes-page"),
    path('student/<int:id>/calendar/', coursesViews.StudentSchedule, name="student-schedule-page"),
    path('', include("Courses.urls")),
]
