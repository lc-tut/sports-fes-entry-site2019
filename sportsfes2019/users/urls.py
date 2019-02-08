from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserRecordView.as_view(), name="user_list_create"),
    path('users/<str:number>/', views.UserDetailView.as_view(), name="user_detail_edit_delete"),
    path('teams/', views.TeamRecordView.as_view(), name="team_ilst_create"),
    path('teams/<str:name>/', views.TeamDetailView.as_view(), name="team_detail_edit_delete"),
]