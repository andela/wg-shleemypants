# -*- coding: utf-8 *-*

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

import datetime

import os
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.management.base import BaseCommand, CommandError
from wger.core.models import UserProfile, Language
from django.contrib.auth import authenticate


class Command(BaseCommand):
    """
    Custom command to list users created through api by the specified user
    """

    help = 'Prints list of users created by user specified'

    def handle(self, **options):
        username = options.get('username')

        if not username:
            self.stdout.write(self.style.ERROR(
                'Please fill in username '
                ' \n Example: ./manage.py \
                list-user-rest-api --username admin '
                ''))
            return
        try:
            creator = User.objects.get(username=username[0])

        except User.DoesNotExist:
            raise CommandError('User {} Does not exist in our system'.format(username[0]))

        users = UserProfile.objects.filter(created_by=creator.username)
        if users.count() > 0:
            os.system('clear')
            for profile in users:
                print("###############################  USERS CREATED BY {} ##########################".format(
                    username[0]))
                print("Username : {} \nEmail : {} \n------------------------------------------------------".format(
                    profile.user.username, profile.user.email))
        else:
            print("########## USER {} HAS NOT CREATED ANY USER VIA API #############".format(username[0]))

    def add_arguments(self, parser):
        parser.add_argument('--username', nargs='+', type=str)
        parser.add_argument('--password', nargs='+', type=str)

#
# api_user_email = input("Please input Their Email \n")
#             api_user_password = input("Please input their password \n")
