from .models import Team, Member
from .serializers import TeamSerializer, MemberSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import APIException
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

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
            raise APIException("Leader should not be deleted. You can delete leader only when deleting the team.")

        instance.delete()