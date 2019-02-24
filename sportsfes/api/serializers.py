from rest_framework import serializers
from .models import *
from drf_writable_nested import WritableNestedModelSerializer

class MemberSerializer(serializers.ModelSerializer):
    team = serializers.StringRelatedField()

    class Meta:
        model = Member
        fields = ('pk', 'name', 'email', 'grade', 'experience', 'team')


class TeamSerializer(serializers.ModelSerializer):
    leader = MemberSerializer()
    members = MemberSerializer(many=True, read_only=True, required=False)

    created_by = serializers.ReadOnlyField(source='created_by.name')
    
    class Meta:
        model = Team
        fields = ('pk', 'name', 'created_by', 'event', 'leader', 'members')

    def create(self, validated_data):
        leader_data = validated_data.pop('leader')
        team = Team.objects.create(**validated_data)
        leader = Member.objects.create(team=team, **leader_data)
        team.leader = leader
        team.save()
        return team
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.event = validated_data.get('event', instance.event)
        instance.save()

        leader_data = validated_data.get('leader', None)

        instance.leader.name = leader_data.get('name', instance.leader.name)
        instance.leader.email = leader_data.get('email', instance.leader.email)
        instance.leader.grade = leader_data.get('grade', instance.leader.grade)
        instance.leader.experience = leader_data.get('experience', instance.leader.experience)
        instance.leader.save()

        

        return instance