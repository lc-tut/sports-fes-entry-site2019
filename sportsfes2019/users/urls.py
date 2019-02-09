from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserRecordView.as_view(), name="user_list_create"),
    path('users/<str:number>/', views.UserDetailView.as_view(), name="user_detail_edit_delete"),
    path('teams/', views.TeamRecordView.as_view(), name="team_ilst_create"),
    path('teams/<str:name>/', views.TeamDetailView.as_view(), name="team_detail_edit_delete"),
    path('teams/<str:name>/members/', views.MemberRecordView.as_view(), name="member_list_create"),
    path('teams/<str:name>/members/<str:number>/', views.MemberDetailView.as_view(), name="member_detail_edit_delete"),
    path('teams/<str:name>/leader/', views.LeaderDetailView.as_view(), name="leader_detail_edit"),
]