# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Workout Manager.  If not, see <http://www.gnu.org/licenses/>.
from django.contrib.auth.models import User
from rest_framework import serializers

from wger.core.models import (
    UserProfile,
    Language,
    DaysOfWeek,
    License,
    RepetitionUnit,
    WeightUnit)


class UserprofileSerializer(serializers.ModelSerializer):
    '''
    Workout session serializer
    '''

    class Meta:
        model = UserProfile


# helper function to ensure that field is not empty
def requiredField(value):
    if not value:
        raise serializers.ValidationError('This field is required')


class UserSerializer(serializers.ModelSerializer):
    """
    API USER Serializer
    """
    # marking email as required
    email = serializers.EmailValidator()

    def create(self, validated_data):
        creator = self.context['request'].user
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        user.userprofile.created_by = creator.username
        user.userprofile.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class UsernameSerializer(serializers.Serializer):
    '''
    Serializer to extract the username
    '''
    username = serializers.CharField()


class LanguageSerializer(serializers.ModelSerializer):
    '''
    Language serializer
    '''

    class Meta:
        model = Language


class DaysOfWeekSerializer(serializers.ModelSerializer):
    '''
    DaysOfWeek serializer
    '''

    class Meta:
        model = DaysOfWeek


class LicenseSerializer(serializers.ModelSerializer):
    '''
    License serializer
    '''

    class Meta:
        model = License


class RepetitionUnitSerializer(serializers.ModelSerializer):
    '''
    Repetition unit serializer
    '''

    class Meta:
        model = RepetitionUnit


class WeightUnitSerializer(serializers.ModelSerializer):
    '''
    Weight unit serializer
    '''

    class Meta:
        model = WeightUnit
