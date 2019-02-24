from .models import Team, Member
from .serializers import TeamSerializer, MemberSerializer
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status

class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(created_by=self.request.user)
        else:
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


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
        serializer.save(team=team)


class MemberDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MemberSerializer
    lookup_url_kwargs = "pk"

    def get_queryset(self):
        pk = self.kwargs.get(self.lookup_url_kwargs)
        members = Member.objects.filter(team_id=pk)
        return members