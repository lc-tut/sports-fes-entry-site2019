from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import *
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from django.conf import settings
import random
import string
from datetime import datetime
import copy


def create_valid_team_data():
    fake_en = Faker()
    fake_ja = Faker('ja_JP')
    data = dict()
    
    while True:
        data['name'] = random.choice([fake_en.company(), fake_ja.word()])

        if 0 < len(data['name']) <= 50:
            break

    choices = [choice[0] for choice in Team.EVENT_CHOICES]
    data['event'] = random.choice(choices)
    data['leader'] = create_valid_member_data()

    number_of_members = random.randint(settings.NUMBER_OF_MEMBERS[data['event']][0] - 1, settings.NUMBER_OF_MEMBERS[data['event']][1] - 1)

    while True:
        data['members'] = []
        for i in range(number_of_members):
            data['members'].append(create_valid_member_data())
        
        experiences = [member['experience'] for member in data['members']]
        experiences.append(data['leader']['experience'])
        if not settings.BEGINNER_AND_EXPERIENCED[data['event']]:
            break
        elif (True in experiences) and (False in experiences):
            break

    return data

def create_valid_member_data():
    fake = Faker('ja_JP')
    data = dict()
    while True:
        data['name'] = random.choice([fake.name(), fake.user_name()])

        if 0 < len(data['name']) <= 100:
            break
    
    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    email += random.choice(string.digits)
    email += '1'
    email += str(random.randint(0, datetime.now().year % 100)).zfill(2)
    for i in range(5):
        email += random.choice(string.digits)
    email += '@edu.teu.ac.jp'
    data['email'] = email

    data['experience'] = random.choice([True, False])
    
    return data

def get_valid_member_data(member_data):
    data = copy.deepcopy(member_data)
    data['name'] = 'a' * 100
    yield data

    data['name'] = 'あ' * 100
    yield data

    data = copy.deepcopy(member_data)
    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    number = ''
    for i in range(9):
        number += random.choice(string.digits)
    email += number
    email += '@edu.teu.ac.jp'
    data['email'] = email
    yield data

    data = copy.deepcopy(member_data)
    data['experience'] = random.choice([True, False])
    yield data

def get_invalid_member_data(member_data):
    data = copy.deepcopy(member_data)
    del data['name']
    yield data

    data['name'] = ''
    yield data

    data['name'] = 'a' * 101
    yield data

    data = copy.deepcopy(member_data)
    del data['email']
    yield data

    data['email'] = ''
    yield data

    data = copy.deepcopy(member_data)
    data['email'][0] = 'z'
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(8)
        email += random.choice(string.digits)
    email += '@edu.teu.ac.jp'
    data['email'] = email
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(10)
        email += random.choice(string.digits)
    email += '@edu.teu.ac.jp'
    data['email'] = email
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(9)
        email += random.choice(string.digits)
    email += '@gmail.com'
    data['email'] = email
    yield data

    data = copy.deepcopy(member_data)
    del data['experience']
    yield data

    data['experience'] = ''
    yield data

    data['experience'] = 'a'
    yield data

def get_valid_team_data(team_data):
    data = copy.deepcopy(team_data)
    data['name'] = 'a' * 50
    yield data

    data['name'] = 'あ' * 50
    yield data

def get_invalid_team_data(team_data):
    data = copy.deepcopy(team_data)
    del data['name']
    yield data

    data['name'] = ''
    yield data

    data['name'] = 'a' * 51
    yield data

    data = copy.deepcopy(team_data)
    data['event'] = 'Golf'
    yield data

    data['event'] = 'soccer'
    yield data


class TeamListTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')


    def test_team_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_team_creation_with_valid_name(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()
        
        data['name'] = 'a' * 50
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

        data['name'] = 'あ' * 50
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_team_creation_with_invalid_name(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        del data['name']
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 0)

        data['name'] = ''
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 0)

        data['name'] = 'a' * 51
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_creation_with_invalid_event(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        data['event'] = 'Golf'
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 0)

        data['event'] = 'soccer'
        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_creation_with_valid_leader_data(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        self.



