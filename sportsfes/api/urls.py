from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
     path('teams/', views.TeamList.as_view(), name='team-list'),
     path('teams/<int:pk>/', views.TeamDetail.as_view(), name='team-detail'),
     path('teams/<int:pk>/members/', views.MemberList.as_view(), name='member-list'),
     path('teams/<int:pk>/members/<int:member_pk>/', views.MemberDetail.as_view(), name='member-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)