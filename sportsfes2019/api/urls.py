from django.urls import path

from . import views

urlpatterns = [
    path('students/', views.MemberRecordView.as_view(), name="member_list_create"),
    path('students/<str:number>/', views.MemberDetailView.as_view(), name="member_detail_edit_delete"),
]