from .models import Team, Member
from .serializers import TeamSerializer, MemberSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .exceptions import APIException
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from rest_framework.decorators import api_view, permission_classes
from google.oauth2 import id_token
from google.auth.transport import requests
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import DoesRequestUserOwnTeam, DoesRequestUserOwnTeamOneBelongs
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from django.views.generic import TemplateView
import datetime
import numpy as np
import re
from .jobs import send_mail
from django.utils.decorators import decorator_from_middleware
import django_rq
import json


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )


    def list(self, request, *args, **kwargs):
        
        queryset = self.filter_queryset(self.queryset.filter(created_by=request.user, is_registered=True))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):

        if not 'members' in serializer.validated_data or len(serializer.validated_data['members']) + 1 < settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0] or len(serializer.validated_data['members']) + 1 > settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]:
            raise APIException("invalid number of members. min: " + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0]) + ' max: ' + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]))

        if settings.BEGINNER_AND_EXPERIENCED[serializer.validated_data['event']]:
            experiences = [member['experience'] for member in serializer.validated_data['members']]
            experiences.append(serializer.validated_data['leader']['experience'])

            if (True not in experiences) or (False not in experiences):
                raise APIException("At least one beginner and one experienced person must be in the team")

        now = datetime.datetime.now()

        if settings.DRAWING_LOTS_DATE < now < settings.ENTRY_DEADLINE_DATE and Team.objects.filter(event=serializer.validated_data['event'], is_registered=True).count() >= settings.NUMBER_OF_TEAMS[serializer.validated_data['event']]:
            raise APIException("Number of teams has already reached the limit")


        team = serializer.save(created_by=self.request.user)

        #send_mail('team-create', team=team)
        django_rq.enqueue(send_mail, 'team-create', team=team)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, DoesRequestUserOwnTeam, )

    def perform_update(self, serializer):
        team = self.get_object()

        if 'members' in serializer.validated_data: 
            # update members information 
            # after removing old members information

            if len(serializer.validated_data['members']) + 1 < settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0] or len(serializer.validated_data['members']) + 1 > settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]:
                raise APIException("invalid number of members. min: " + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0]) + ' max: ' + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]))
            
            if settings.BEGINNER_AND_EXPERIENCED[serializer.validated_data['event']]:
                experiences = [member['experience'] for member in serializer.validated_data['members']]
                experiences.append(serializer.validated_data['leader']['experience'])

                if (True not in experiences) or (False not in experiences):
                    raise APIException("At least one beginner and one experienced person must be in the team")

            for member in team.members.all():
                if not member == team.leader:
                    member.delete()

        else:
            if len(team.members.all()) < settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0] or len(team.members.all()) > settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]:
                raise APIException("invalid number of members. min: " + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][0]) + ' max: ' + str(settings.NUMBER_OF_MEMBERS[serializer.validated_data['event']][1]))

            if settings.BEGINNER_AND_EXPERIENCED[serializer.validated_data['event']]:
                experiences = []
                for member in team.members.all():

                    if team.leader == member:
                        experiences.append(serializer.validated_data['leader']['experience'])
                    else:
                        experiences.append(member.experience)

                if not True in experiences or not False in experiences:
                    raise APIException("At least one beginner and one experienced person must be in the team")

        serializer.save()

        #send_mail('team-update', team=team)
        django_rq.enqueue(send_mail, 'team-update', team=team)

    def perform_destroy(self, instance):
        #send_mail('team-delete', team=instance)
        django_rq.enqueue(send_mail, 'team-delete', team=instance)
        instance.delete()


class MemberList(generics.ListCreateAPIView):
    serializer_class = MemberSerializer
    lookup_url_kwargs = "pk"
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, DoesRequestUserOwnTeam)

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwargs)
        team = get_object_or_404(Team, pk=pk)
        self.check_object_permissions(self.request, team)
        members = Member.objects.filter(team_id=pk)
        return members

    def perform_create(self, serializer):
        pk = self.kwargs.get(self.lookup_url_kwargs)
        team = get_object_or_404(Team, pk=pk)
        self.check_object_permissions(self.request, team)
        if len(team.members.all()) >= settings.NUMBER_OF_MEMBERS[team.event][1]:
            raise APIException("Your team already has max number of members")

        member = serializer.save(team=team)

        #send_mail('member-create', member_changed=member)
        django_rq.enqueue(send_mail, 'member-create', member_changed=member)

class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    lookup_url_kwarg = 'member_pk'
    lookup_field = 'pk'
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, DoesRequestUserOwnTeamOneBelongs, )

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

        member = serializer.save()

        #send_mail('member-update', member_changed=member)
        django_rq.enqueue(send_mail, 'member-update', member_changed=member)

    def perform_destroy(self, instance):
        team = get_object_or_404(Team, pk=self.kwargs.get(self.lookup_field))
        if team.leader == instance:
            raise APIException("Leader should not be deleted. You can delete leader only when deleting the team.")
        
        if len(team.members.all()) <= settings.NUMBER_OF_MEMBERS[team.event][0]:
            raise APIException("You cannot delete member because You must have at least " + str(settings.NUMBER_OF_MEMBERS[team.event][0]) + " members")

        #send_mail('member-delete', member_changed=instance)
        django_rq.enqueue(send_mail, 'member-delete', member_changed=instance)
        instance.delete()



########## login ##########
@api_view(['GET', 'POST', 'OPTION'])
@permission_classes((AllowAny, ))
#@decorator_from_middleware(shortcircuitmiddleware)
def token_signin_view(request):
    if request.method == 'GET':
        return HttpResponse('hello')
    else:
        token = request.POST.get('idtoken', None)

        if token == None:
            raise APIException('idtoken is required')

        idinfo = id_token.verify_oauth2_token(token, requests.Request(), settings.CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accouts.google.com']:
            raise APIException('Wrong issuer.')

        pattern = r"[bcemdh]\d{9}@edu.teu.ac.jp"  
        if not re.match(pattern, idinfo['email']):
            raise APIException("invalid email. use xxxxx@edu.teu.ac.jp")
        

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
@permission_classes((AllowAny, ))
#@decorator_from_middleware(shortcircuitmiddleware)
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


########## /registerable ##########
@api_view(['GET'])
@permission_classes((AllowAny, ))
def is_registerable(request):
    response = HttpResponse()
    
    event_list = [event[0] for event in Team.EVENT_CHOICES]

    data = {}

    for event in event_list:
        if not (settings.DRAWING_LOTS_DATE < datetime.datetime.now() < settings.ENTRY_DEADLINE_DATE):
            data[event] = 'false'
        else:
            if Team.objects.filter(event=event, is_registered=True).count() >= settings.NUMBER_OF_TEAMS[event]:
                data[event] = 'false'
            else:
                data[event] = 'true'

    data = json.dumps(data)
    response.write(data)

    return response        

########## root page of api application ##########
class IndexTemplateView(TemplateView):
    template_name = "index.html"
