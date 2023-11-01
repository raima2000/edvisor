from django.urls import path
from . import views

urlpatterns = [
    path("view/", views.ClassworkView, name='classwork-view'),
    path("<int:test_id>/list/", views.SubmittedListView, name='submitted-view'),
    path("create/",views.CreateClassworkView, name='create-classwork-view'),
    path("<int:test_id>/edit/",views.EditClassworkView, name='edit-classwork-view'),
    path("<int:test_id>/download/",views.DownloadTestFile, name = "download-test-file"),
    path("<int:test_id>/change/",views.ChangeTestInformation, name = 'change-test-information'),
    path("<int:test_id>/do/",views.DoTestView,name='do-test'),
    path("<int:test_id>/upload/",views.UploadAssignmentview,name='upload-assignment'),
    path("<int:test_id>/edit/addwritten/",views.written_question_form,name='written-form'),
    path("<int:test_id>/edit/addmultiplechoice/",views.multiplechoice_form,name='multiplechoice-form'),
    path("<str:qid>/mcoform/",views.mco_form,name='mco-form'),
    path("<int:test_id>/delete/",views.DeleteTest,name='delete-classwork-view'),
    path("<int:test_id>/<int:qid>/delete",views.DeleteQuestion,name='delete-question-view'),
    path("<int:test_id>/<int:qid>/update",views.UpdateQuestion,name='update-question-view'),
    path("view/<int:studenttest_id>/",views.ViewStudentTest,name='view-student-test'),
    path("view/<int:studenttest_id>/download/",views.DownloadStudentFile,name='download-student-file')
]