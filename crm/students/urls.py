from django.urls import path

from . import views

urlpatterns = [

    path('dashboard/',views.DashboardView.as_view(),name='dashboard'),

    path('students-list/',views.StudentListView.as_view(),name='students-list'),

    path('add-student/',views.AddStudent.as_view(),name='add-student'),
    
    path('student-details/<str:uuid>/',views.StudentDetailsView.as_view(),name='student-details'),

    path('student-delete/<str:uuid>/',views.StudentDeleteView.as_view(),name='student-delete'),

    path('student-edit/<str:uuid>/',views.EditStudent.as_view(),name='student-edit'),
    


]

