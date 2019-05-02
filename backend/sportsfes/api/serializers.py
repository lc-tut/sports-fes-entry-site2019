from rest_framework import serializers
from .models import *
import re
from datetime import datetime
from django.conf import settings

class MemberSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()

    class Meta:
        model = Member
        fields = ('pk', 'name', 'email', 'experience', 'team')

    def validate_email(self, data):
        pattern = r"[bcemdh]\d{7}[a-z0-9]{2}@edu.teu.ac.jp"  
        if not re.match(pattern, data):
            raise serializers.ValidationError("invalid email. use xxxxx@edu.teu.ac.jp")
        
        return data


class TeamSerializer(serializers.ModelSerializer):
    leader = MemberSerializer()
    members = MemberSerializer(many=True, required=False)

    created_by = serializers.ReadOnlyField(source='created_by.name')
    
    class Meta:
        model = Team
        fields = ('pk', 'name', 'created_by', 'event', 'leader', 'members')

    def create(self, validated_data):
        leader_data = validated_data.pop('leader')
        members_data = validated_data.pop('members')

        leader = Member.objects.create(**leader_data)

        now = datetime.now()

        team = Team.objects.create(leader=leader, is_registered=True, **validated_data)
            
        leader.team = team
        leader.save()

        for member_data in members_data:
            Member.objects.create(team=team, **member_data)

        team.save()
        return team
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.event = validated_data.get('event', instance.event)
        instance.save()

        leader_data = validated_data.get('leader', None)

        instance.leader.name = leader_data.get('name', instance.leader.name)
        instance.leader.email = leader_data.get('email', instance.leader.email)
        instance.leader.experience = leader_data.get('experience', instance.leader.experience)
        instance.leader.save()

        if 'members' in validated_data:
            for member_data in validated_data.pop('members'):
                Member.objects.create(team=instance, **member_data)

    
        return instance

    def validate(self, data):
        if 'members' in data:
            members_data = data['members']

            for member_data in members_data:
                member_serializer = MemberSerializer(data=member_data)
                if not member_serializer.is_valid():
                    raise serializers.ValidationError("invalid members data")
        
        return data