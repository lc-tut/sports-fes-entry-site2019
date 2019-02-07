from .serializer import *
from .models import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class MemberRecordView(APIView):
    """
    A class based view for creating and fetching member records
    """
    def get(self, format=None):
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """
        Create a member record
        """

        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)


class MemberDetailView(APIView):
    def get_object(self, number):
        try:
            return Member.objects.get(number=number)
        except Member.DoesNotExist:
            raise Http404

    def get(self, request, number, format=None):
        member = self.get_object(number)
        serializer = MemberSerializer(member)
        return Response(serializer.data)

    def put(self, request, number, format=None):
        member = self.get_object(number)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.update(member, validated_data=request.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, number, format=None):
        member = self.get_object(number)
        member.user.delete()
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)