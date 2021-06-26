from django.db import models
from django.db.models import fields
from rest_framework import serializers
from app.models import  Reports, User,Shouts,Friends

""" class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userId',
                  'userName',
                  'emailId',
                  'password',
                  'admin_verify') """

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('userId',
                  'userName',
                  'emailId',
                  'password',
                  'admin_verify',
                  'firstName',
                  'lastName',
                  'DateOfBirth',
                  'MobileNo',
                  'profilePic')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ShoutSerializer(serializers.ModelSerializer):
    class Meta:
        model= Shouts
        fields=(
            'shoutId',
            'userId',
            'path',
            'caption',
            'type',
            'uploadDate'
        )

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Friends
        fields=(
            
            'userId',
            'friendId',
            'status'
        )
class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reports
        fields=(
            'reportId',
            'shoutId',
            'userId',
            'reason'
        )



