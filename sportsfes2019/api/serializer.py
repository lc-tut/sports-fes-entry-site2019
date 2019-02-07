from rest_framework import serializers, status
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ('username', 'email')


class MemberSerializer(serializers.ModelSerializer):
    """
    A Member Serializer to return the student details
    """

    user = UserSerializer(required=True)

    class Meta:
        model = Member
        fields = ('number', 'user', 'grade', 'experience',)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        member, _ = Member.objects.update_or_create(number=validated_data.pop('number'), user=user, grade=validated_data.pop('grade'), experience=validated_data.pop('experience'))
        return member


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        instance.grade = validated_data.get('grade', instance.grade)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.save()

        user = instance.user
        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance