from rest_framework import serializers


class MemberSerializer(serializers.HyperlinkedModelSerializer):


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    leader = serializers.HyperlinkedIdentityField(view_name='member-detail')
    created_by = serializers.HyperlinkedIdentityField(view_name='user-detail')
    members = serializers.HyperlinkedIdentityField(many=True, view_name='member-detail')    

    