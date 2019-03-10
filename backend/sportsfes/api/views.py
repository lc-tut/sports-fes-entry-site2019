from .models import Team, Member
from .serializers import TeamSerializer, MemberSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from api.permissions import HasUserIdInSessionForTeam
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from django.views.generic import TemplateView

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):

        if len(serializer.validated_data['members']) < settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0] or len(serializer.validated_data['members']) > settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]:
            raise APIException("invalid number of members. min: " + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0]) + ' max: ' + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]))

        if settings.BEGINNER_AND_EXPERIENCED[serializer.validated_data['event']]:
            experiences = [member['experience'] for member in serializer.validated_data['members']]
            if not True in experiences or not False in experiences:
                raise APIException("At least one beginner and one experienced person must be in the team")

        serializer.save(created_by=self.request.user)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def perform_update(self, serializer):
        if 'members' in serializer.validated_data:
            raise APIException("members are not needed")

        if settings.BEGINNER_AND_EXPERIENCED[serializer.validated_data['event']]:
            team = self.get_object()
            experiences = []
            for member in team.members.all():

                if team.leader == member:
                    experiences.append(serializer.validated_data['leader']['experience'])
                else:
                    experiences.append(member.experience)

            if not True in experiences or not False in experiences:
                raise APIException("At least one beginner and one experienced person must be in the team")

        serializer.save()


class MemberList(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    lookup_url_kwargs = "pk"
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwargs)
        members = Member.objects.filter(team_id=pk)
        return members

    def perform_create(self, serializer):
        pk = self.kwargs.get(self.lookup_url_kwargs)
        team = get_object_or_404(Team, pk=pk)
        if len(team.members.all()) >= settings.NUMBER_OF_MEMBERS[team.event][1]:
            raise APIException("Your team already has max number of members")

        serializer.save(team=team)

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    lookup_url_kwarg = 'member_pk'
    lookup_field = 'pk'
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        members = Member.objects.filter(team_id=self.kwargs[self.lookup_field])
        return members

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def perform_update(self, serializer):
        team = get_object_or_404(Team, pk=self.kwargs.get(self.lookup_field))
        if team.leader == self.get_object():
            raise APIException("Information of leader should not be updated here. Use /api/teams/<pk>/ (PUT) instead.")

        if settings.BEGINNER_AND_EXPERIENCED[team.event]:
            experiences = []
            for member in team.members.all():
                if member == self.get_object():
                    experiences.append(serializer.validated_data['experience'])
                else:
                    experiences.append(member.experience)

            if not True in experiences or not False in experiences:
                raise APIException("At least one beginner and one experienced person must be in the team")

        serializer.save()

    def perform_destroy(self, instance):
        team = get_object_or_404(Team, pk=self.kwargs.get(self.lookup_field))
        if team.leader == instance:
            raise APbIException("Leader should not be deleted. You can delete leader only when deleting the team.")

        instance.delete()


########## login ##########
@api_view(['GET', 'POST', 'OPTION'])
@permission_classes(())
def token_signin_view(request):
    if request.method == 'GET':
        return HttpResponse('hello')
    else:
        token = request.POST['idtoken']

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accouts.google.com']:
            raise APIException('Wrong issuer.')

        user, created = User.objects.get_or_create(
            email=idinfo['email'],
            defaults={'username': idinfo['name']}
        )

        user.save()
        login(request, user)
        request.session['user_id'] = idinfo['sub']
        request.session.set_expiry(60 * 60 * 24 * 365)
        request.session.set_test_cookie()        

        response = HttpResponse()
        message = 'yes\r\n' if request.user.is_authenticated else 'no\r\n' 
        message2 = 'yes\r\n' if request.session.test_cookie_worked() else 'no\r\n'
        response.write(message)
        response.write(message2)
        response.write(request.user.username + "\r\n")

        return response

########## logout ###########
@api_view(['POST'])
def token_logout_view(request):
    response = HttpResponse()
    response.write(request.user.username + '\r\n')
    if request.user.is_authenticated:
        response.set_cookie('sessionid', domain='localhost', max_age=1)
        response.set_cookie('csrftoken', domain='localhost', max_age=1)
        response.write('logged out')
        logout(request)
    else:
        response.write('you have not logged in')

    return response

########## root page of api application ##########
class IndexTemplateView(TemplateView):
    template_name = "index.html"