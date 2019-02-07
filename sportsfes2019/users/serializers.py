from rest_framework import serializers, status
from .models import User



class UserSerializer(serializers.ModelSerializer):
    """
    A User Serializer to return the student details
    """

    class Meta:
        model = User
        fields = ('number', 'username', 'email', 'grade', 'experience',)

    def create(self, validated_data):
        user, _ = User.objects.create_user(number=validated_data.pop('number'), username=validated_data.pop('username'), email=validated_data.pop('email'), grade=validated_data.pop('grade'), experience=validated_data.pop('experience'))
        return user


    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.save()

        return instance