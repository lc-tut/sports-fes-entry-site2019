from rest_framework import serializers, status
from .models import User, Team



class UserSerializer(serializers.ModelSerializer):
    """
    A User Serializer to return the student details
    """

    class Meta:
        model = User
        fields = ('number', 'username', 'email', 'grade', 'experience',)

    def create(self, validated_data):
        user = User.objects.update_create(number=validated_data.pop('number'), username=validated_data.pop('username'), email=validated_data.pop('email'), grade=validated_data.pop('grade'), experience=validated_data.pop('experience'))
        return user


    def update(self, instance, validated_data):
        """
        if updater is not user's leader, this function does not update user information
        """
        instance.number = validated_data.get('number', instance.number)
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.experience = validated_data.get('experience', instance.experience)
        instance.save()

        return instance


class TeamSerializer(serializers.ModelSerializer):
    """
    A Team Serializer to return the information of the team
    """
    leader = UserSerializer(required=False)
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Team
        fields = ('name', 'event', 'leader', 'members')

    """
    def update_user(user_data):
        try:
            user = User.objects.get(email=user_data.pop('email'))
        except User.DoesNotExist:
            user = None

        if not (user == None):
            user = UserSerializer(UserSerializer(), user, user_data)
        
        return user
    """

    def create(self, validated_data):
        leader_data = validated_data.pop('leader')
        members_data = validated_data.pop('members')
        leader = User.objects.get_create(number=leader_data.pop('number'), username=leader_data.pop('username'), email=leader_data.pop('email'), grade=leader_data.pop('grade'), experience=leader_data.pop('experience'))
        team = Team.objects.create(name=validated_data.pop('name'), event=validated_data.pop('event'), leader=leader)

        for member_data in members_data:
            User.objects.get_create(number=member_data.pop('number'), username=member_data.pop('username'), email=member_data.pop('email'), grade=member_data.pop('grade'), experience=member_data.pop('experience') ,team=team)

        return team

    """
    def update(self, instance, validated_data):
        
        if updater is not the creater of the team, team's information cannot be updated
        
        instance.name = validated_data.get('name', instance.name)
        instance.event = validated_data.get('event', instance.event)

        instance.save()

        leader_data = validated_data.pop('leader')
        leader = self.update_user(leader_data)
        
        members_data = validated_data.pop('members')
        for member_data in members_data:
            self.update_user(member_data)

        return instance
    """