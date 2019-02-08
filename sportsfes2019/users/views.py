from django.shortcuts import render
from .serializers import *
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserRecordView(APIView):
    # A class based view for creating and fetching user records

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
    #    Create a user record

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    def get_object(self, number):
        try:
            return User.objects.get(number=number)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, number, format=None):
        user = self.get_object(number)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, number, format=None):
        user = self.get_object(number)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.update(user, validated_data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number, format=None):
        user = self.get_object(number)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamRecordView(APIView):
    # A class based view for creating and fetching team records

    def get(self, format=None):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    
    def post(self, request):
    #    Create a user record

        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class TeamDetailView(APIView):
    def get_object(self, name):
        try:
            return Team.objects.get(name=name)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, name, format=None):
        team = self.get_object(name)
        serializer = TeamSerializer(team)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        team = self.get_object(name)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.update(team, validated_data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, format=None):
        team = self.get_object(name)
        for user in team.members.all():
            user.delete()

        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
