from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .serializers import *
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken,models import Token
from oauth2client import client, crypt


class UserRecordView(APIView):
    # A class based view for creating and fetching user records

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    

class UserDetailView(APIView):

    def get(self, request, number, format=None):
        user = get_object_or_404(User, number=number)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, number):
        user = get_object_or_404(User, number=number)
        user.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamRecordView(APIView):
    # A class based view for creating and fetching team records

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

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

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, format=None):
        team = get_object_or_404(Team, name=name)
        serializer = TeamSerializer(team)
        return Response(serializer.data)


    def put(self, request, name, format=None):
        team = get_object_or_404(Team, name=name)
        serializer = TeamSerializer(team, data=request.data)
        if serializer.is_valid():
            #serializer.update(team, validated_data=request.data)
            team.name = request.data.pop('name')
            team.event = request.data.pop('event')
            team.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, name, format=None):
        team = get_object_or_404(Team, name=name)
        team.leader.delete()
        for user in team.members.all():
            user.delete()

        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MemberRecordView(APIView):
    # A class based view for creating and fetching user records

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, format=None):
        users = User.objects.all().filter(team__name=name)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, name):
    #    Create a user record
        team = get_object_or_404(Team, name=name)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            member = serializer.create(validated_data=request.data)
            member.team = team
            member.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    

class MemberDetailView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, number, format=None):
        user = get_object_or_404(User, number=number)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, name, number, format=None):
        user = get_object_or_404(User, number=number)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.update(user, validated_data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, name, number, format=None):
        user = get_object_or_404(User, number=number)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LeaderDetailView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, name, format=None):
        user = get_object_or_404(Team, name=name).leader
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, name, format=None):
        user = get_object_or_404(Team, name=name).leader
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.update(user, validated_data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    def verifyGoogleToken(self, idToken):
        isIdTokenValid = True
        try:
            idinfo = client.verify_id_token(idToken, settings.CLIENT_ID)
        except crypt.AppIdentityError:
            isIdTokenValid = False
            idinfo = [
                'Response': 'Invalid Google Token!',
            ]
        return (isIdTokenValid, idinfo)
    
    def post(self, request, format=None):
        isIdTokenValid, googleResponse = self.verifyGoogleToken(request.data.get('id_token'))
        if isIdTokenValid:
            try:
                user = User.objects.get(email=googleResponse.get('email'))
                token = Token.objects.get(user=user)
                statusCode = status.HTTP_202_ACCEPTED
            except User.DoesNotExist:
                user = User.objects.create_user(username=googleResponse.get('name'), email=googleResponse.get('email'), number=googleResponse.get('email').split('@')[0], grade=1, experience=False)
                token = Token.objects.create(user=user)
                statusCode = status.HTTP_201_CREATED
            
            additionalContent = [
                'token': token.key,
            ]
            googleResponse.update(additionalContent)
            return Response(googleResponse, statusCode)
        else:
            return Response(googleResponse, status=status.HTTP_400_BAD_REQUEST)