from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from api import jobs


app_name = 'api'
urlpatterns = [
     path('', views.IndexTemplateView.as_view(), name='index'),
     path('registerable/', views.is_registerable, name='registerable'),
     path('emails/', views.member_emails_view, name="member-email"),
     path('teams/', views.TeamList.as_view(), name='team-list'),
     path('teams/<int:pk>/', views.TeamDetail.as_view(), name='team-detail'),
     path('teams/<int:pk>/members/', views.MemberList.as_view(), name='member-list'),
     path('teams/<int:pk>/members/<int:member_pk>/', views.MemberDetail.as_view(), name='member-detail'),
     path('tokensignin/', views.token_signin_view, name='tokensignin'),
     path('tokenlogout/', views.token_logout_view, name='tokenlogout'),
]

urlpatterns = format_suffix_patterns(urlpatterns)