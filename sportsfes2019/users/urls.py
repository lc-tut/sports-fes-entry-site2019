from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UserRecordView.as_view(), name="user_list_create"),
    path('users/<str:number>/', views.UserDetailView.as_view(), name="user_detail_edit_delete"),
]