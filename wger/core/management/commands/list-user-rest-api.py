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

from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.management.base import BaseCommand, CommandError
from wger.core.models import UserProfile, Language
from django.contrib.auth import authenticate


class Command(BaseCommand):
    """
    Nice and awesome way to print your name in CMD, it doesn't have to be ugly
    """

    help = 'Prints your name when you type it'

    def handle(self, **options):
        username = options.get('username')
        password = options.get('password')

        if not username or not password:
            self.stdout.write(self.style.ERROR('Please fill in username and password \n Example: ./manage.py '
                                               'sample-cmd --username admin --password kibua'))
        admin = authenticate(username=username[0], password=password[0])
        if admin:
            self.stdout.write(self.style.SUCCESS('Welcome {} \n'.format(username[0])))
            api_user_name = input("Please input username you wish to grant access to creating API User \n")
            print("creating an account for {} with email and password ".format(api_user_name))
        else:
            self.stdout.write(self.style.ERROR('Authentication Failed, Bad Credentials for {} '.format(username[0])))
            return

        try:
            user = User.objects.get(username=api_user_name)
            if getattr(user.userprofile, 'can_create_api_user'):
                self.stdout.write(
                    self.style.SUCCESS("User {} already has a permission to create api users".format(api_user_name)))
            else:
                setattr(user.userprofile, 'can_create_api_user', True)
                user.userprofile.save()
                self.stdout.write(self.style.SUCCESS("User {} can now create api users".format(api_user_name)))


        except User.DoesNotExist:
            raise CommandError('{} Does not exist in our system'.format(api_user_name))

    def add_arguments(self, parser):
        parser.add_argument('--username', nargs='+', type=str)
        parser.add_argument('--password', nargs='+', type=str)

#
# api_user_email = input("Please input Their Email \n")
#             api_user_password = input("Please input their password \n")
