from rest_framework import serializers, status
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ('id', 'username', 'first_name', 'last_name', 'email')

class ProfileSerializer(serializers.ModelSerializer):
    """
    A Profile Serializer to return the student details
    """

    user = UserSerializer(required=True)

    class Meta:
        model = Profile
        fields = ('user', 'grade', 'experience',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        profile, _ = Profile.objects.update_or_create(user=user, grade=validated_data.pop('grade'), experience=validated_data.pop('experience'))
        return profile