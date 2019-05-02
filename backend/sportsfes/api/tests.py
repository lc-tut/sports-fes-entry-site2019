from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import *
from api.jobs import *
from django.contrib.auth.models import User
from django.urls import reverse
from faker import Faker
from django.conf import settings
import random
import string
from datetime import datetime
import copy
from datetime import datetime, timedelta
import json
from django.core import mail
import django_rq


def create_valid_team_data(event=None):
    fake_en = Faker()
    fake_ja = Faker('ja_JP')
    data = dict()
    
    while True:
        data['name'] = random.choice([fake_en.company(), fake_ja.word()])

        if 0 < len(data['name']) <= 50:
            break

    choices = [choice[0] for choice in Team.EVENT_CHOICES]

    if event in choices:
        data['event'] = event
    else:
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
    l = list(data['email'])
    l[0] = 'z'
    data['email'] = ''.join(l)
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(8):
        email += random.choice(string.digits)
    email += '@edu.teu.ac.jp'
    data['email'] = email
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(10):
        email += random.choice(string.digits)
    email += '@edu.teu.ac.jp'
    data['email'] = email
    yield data

    email = random.choice(['b', 'c', 'e', 'm', 'd', 'h'])
    for i in range(9):
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

    data = copy.deepcopy(team_data)
    choices = [choice[0] for choice in Team.EVENT_CHOICES]
    data['event'] = random.choice(choices)

    data = copy.deepcopy(team_data)
    for leader_data in get_valid_member_data(data['leader']):
        data['leader'] = leader_data
        yield data

    data['members'] = []
    for i in range(settings.NUMBER_OF_MEMBERS[data['event']][0] - 1):
        data['members'].append(create_valid_member_data())
    yield data

    data['members'] = []
    for i in range(settings.NUMBER_OF_MEMBERS[data['event']][1] - 1):
        data['members'].append(create_valid_member_data())
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

    for leader_data in get_invalid_member_data(data['leader']):
        data['leader'] = leader_data
        yield data

def get_invalid_length_of_members(team_data):
    data = copy.deepcopy(team_data)
    data['members'] = []
    for i in range(settings.NUMBER_OF_MEMBERS[data['event']][0] - 2):
        data['members'].append(create_valid_member_data())
    yield data

    data['members'] = []
    for i in range(settings.NUMBER_OF_MEMBERS[data['event']][1]):
        data['members'].append(create_valid_member_data())
    yield data

def get_valid_team_data_for_updating(team_data):
    data = create_valid_team_data()
    yield data

    data = copy.deepcopy(team_data)
    data['leader'] = create_valid_member_data()
    yield data

    data = copy.deepcopy(team_data)
    del data['members']
    yield data


@override_settings(ENTRY_START_DATE=datetime.now()-timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=10))
class TeamListTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')

    def test_team_creation(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)

    def test_team_creation_without_authentication(self):
        data = create_valid_team_data()

        response = self.client.post(self.url_team_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_creation_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)
        team_data = create_valid_team_data()
        
        for i, data in enumerate(get_valid_team_data(team_data)):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Team.objects.count(), i + 1)

    def test_team_creation_with_invalid_data(self):
        self.client.force_authenticate(user=self.user1)
        team_data = create_valid_team_data()

        for data in get_invalid_team_data(team_data):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Team.objects.count(), 0)

        for data in get_invalid_length_of_members(team_data):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Team.objects.count(), 0)

    def test_team_post_in_each_period(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_mail_after_creating_team(self):
        self.client.force_authenticate(user=self.user1)
        data = create_valid_team_data()

        response = self.client.post(self.url_team_list, data, format='json')
        django_rq.get_worker().work(burst=True)
        self.assertEqual(len(mail.outbox), len(data['members']) + 1)

    def test_post_iooa_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            choices = [choice[0] for choice in Team.EVENT_CHOICES]
            event = random.choice(choices)

            for i in range(settings.NUMBER_OF_TEAMS[event]):
                data = create_valid_team_data(event)
                self.client.post(self.url_team_list, data, format='json')

            data = create_valid_team_data(event)
            response = self.client.post(self.url_team_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_created_team_is_registered(self):
        self.client.force_authenticate(user=self.user1)

        data = create_valid_team_data()
        self.client.post(self.url_team_list, data, format='json')

        self.assertEqual(Team.objects.filter(created_by=self.user1).first().is_registered, True)
 

    def test_team_listing(self):
        self.client.force_authenticate(user=self.user1)
        for i in range(10):
            team_data = create_valid_team_data()
            self.client.post(self.url_team_list, team_data, format='json')
        self.client.logout()

        self.client.force_authenticate(user=self.user2)
        for i in range(10):
            team_data = create_valid_team_data()
            self.client.post(self.url_team_list, team_data, format='json')
        

        response = self.client.get(self.url_team_list)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 10)

        team = Team.objects.filter(created_by=self.user2).first()
        team.is_registered = False
        team.save()

        response = self.client.get(self.url_team_list)
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 9)       

    def test_team_listing_without_authentication(self):
        response = self.client.get(self.url_team_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_list_in_each_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.get(self.url_team_list)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.get(self.url_team_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.get(self.url_team_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)


@override_settings(ENTRY_START_DATE=datetime.now()-timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=10))
class TeamDetailTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')

        self.client.force_authenticate(user=self.user1)
        self.data = create_valid_team_data()
        self.client.post(self.url_team_list, self.data, format='json')        
        self.client.logout()

        self.url_team_detail = reverse('api:team-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk})

    def test_team_updating(self):
        self.client.force_authenticate(user=self.user1)

        for data in get_valid_team_data(self.data):
            self.client.put(self.url_team_detail, self.data, format='json')
            response = self.client.put(self.url_team_detail, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Team.objects.count(), 1)

        for data in get_valid_team_data_for_updating(self.data):
            self.client.put(self.url_team_detail, self.data, format='json')
            response = self.client.put(self.url_team_detail, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Team.objects.count(), 1)

    def test_getting_team_detail_in_each_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.get(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.get(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.get(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_200_OK)        

    def test_updating_team_data_in_each_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.put(self.url_team_detail, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.put(self.url_team_detail, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.put(self.url_team_detail, self.data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_mail_after_updating_team_data(self):
        self.client.force_authenticate(user=self.user1)

        first_number_of_mail = len(mail.outbox)
        self.assertEqual(first_number_of_mail, len(self.data['members']) + 1)

        response = self.client.put(self.url_team_detail, self.data, format='json')
        django_rq.get_worker().work(burst=True)
        self.assertEqual(len(mail.outbox), first_number_of_mail + len(self.data['members']) + 1)

    def test_team_updating_without_authentication(self):
        response = self.client.put(self.url_team_detail, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_team_updating_with_invalid_data(self):
        self.client.force_authenticate(user=self.user1)

        for data in get_invalid_team_data(self.data):
            self.client.put(self.url_team_detail, self.data, format='json')
            response = self.client.put(self.url_team_detail, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Team.objects.count(), 1)

        for data in get_invalid_length_of_members(self.data):
            self.client.put(self.url_team_detail, self.data, format='json')
            response = self.client.put(self.url_team_detail, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Team.objects.count(), 1)
   
    def test_team_deleting(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(self.url_team_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_deleting_in_before_entry_start_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.delete(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_team_deleting_in_after_drawing_lots_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.delete(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_team_deleting_in_after_deadline_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.delete(self.url_team_detail)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_team_deleting_without_authentication(self):
        response = self.client.delete(self.url_team_detail)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.count(), 1)

    def test_sending_mail_after_deleting_team(self):
        self.client.force_authenticate(user=self.user1)

        first_number_of_mail = len(mail.outbox)
        response = self.client.delete(self.url_team_detail)
        django_rq.get_worker().work(burst=True)
        self.assertEqual(len(mail.outbox), first_number_of_mail + len(self.data['members']) + 1)

@override_settings(ENTRY_START_DATE=datetime.now()-timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=10))
class MemberListTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')

        self.client.force_authenticate(user=self.user1)
        self.data = create_valid_team_data()
        self.client.post(self.url_team_list, self.data, format='json')        
        self.client.logout()

        self.url_member_list = reverse('api:member-list', kwargs={'pk': Team.objects.get(name=self.data['name']).pk})

    def test_member_list(self):
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(self.url_member_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_list_without_authentication(self):
        response = self.client.get(self.url_member_list)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_creation(self):
        self.client.force_authenticate(user=self.user1)

        data = create_valid_member_data()
        response = self.client.post(self.url_member_list, data, format='json')

        if len(self.data['members']) < settings.NUMBER_OF_MEMBERS[self.data['event']][1] - 1:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Member.objects.filter(team=Team.objects.get(name=self.data['name'])).count(), len(self.data['members']) + 2)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_list_in_each_period(self):
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.get(self.url_member_list)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.get(self.url_member_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.get(self.url_member_list)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_creation_in_each_period(self):
        self.client.force_authenticate(user=self.user1)

        data = create_valid_member_data()

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.post(self.url_member_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.post(self.url_member_list, data, format='json')

            if len(self.data['members']) < settings.NUMBER_OF_MEMBERS[self.data['event']][1] - 1:
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            else:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.post(self.url_member_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_mail_after_post(self):
        self.client.force_authenticate(user=self.user1)

        data = create_valid_member_data()
        first_number_of_mail = len(mail.outbox)

        response = self.client.post(self.url_member_list, data, format='json')

        if len(self.data['members']) < settings.NUMBER_OF_MEMBERS[self.data['event']][1] - 1:

            django_rq.get_worker().work(burst=True)
            self.assertEqual(len(mail.outbox), first_number_of_mail + len(self.data['members']) + 2)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_member_creation_without_authentication(self):
        data = create_valid_member_data()
        response = self.client.post(self.url_member_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_creation_with_invalid_data(self):
        self.client.force_authenticate(user=self.user1)

        data = create_valid_member_data()
        for data in get_invalid_member_data(data):
            response = self.client.post(self.url_member_list, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(ENTRY_START_DATE=datetime.now()-timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=10))
class MemberDetailTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')

        self.client.force_authenticate(user=self.user1)
        self.data = create_valid_team_data()
        self.client.post(self.url_team_list, self.data, format='json')        
        self.client.logout()

    def test_getting_member_detail(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_member_detail_without_authentication(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_getting_member_detail_in_each_period(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_member_updating(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        member_data = create_valid_member_data()
        for data in get_valid_member_data(member_data):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_member_updating_without_authentication(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})

        member_data = create_valid_member_data()
        response = self.client.put(url, member_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_member_updating_with_invalid_data(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        member_data = create_valid_member_data()
        for data in get_invalid_member_data(member_data):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_updating_in_each_period(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        data = create_valid_member_data()
        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_mail_after_updating_member_data(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        first_number_of_email = len(mail.outbox)
        data = create_valid_member_data()
        response = self.client.put(url, data, format='json')
        django_rq.get_worker().work(burst=True)
        self.assertEqual(len(mail.outbox), first_number_of_email + len(self.data['members']) + 1)


    def test_member_deletion(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(url)
        if len(self.data['members']) > settings.NUMBER_OF_MEMBERS[self.data['event']][0] - 1:
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_deletion_without_authentication(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_leader_deletion(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['leader']['name']).pk})
        self.client.force_authenticate(user=self.user1)

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_deletion_in_each_period(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        with self.settings(ENTRY_START_DATE=datetime.now()+timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=17)):
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=10), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=4)):
            response = self.client.delete(url)
            if len(self.data['members']) > settings.NUMBER_OF_MEMBERS[self.data['event']][0] - 1:
                self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            else:
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        with self.settings(ENTRY_START_DATE=datetime.now()-timedelta(days=17), DRAWING_LOTS_DATE=datetime.now()-timedelta(days=10), ENTRY_DEADLINE_DATE=datetime.now()-timedelta(days=3)):
            response = self.client.delete(url)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_sending_mail_after_deleting_member(self):
        url = reverse('api:member-detail', kwargs={'pk': Team.objects.get(name=self.data['name']).pk, 'member_pk': Member.objects.get(name=self.data['members'][0]['name']).pk})
        self.client.force_authenticate(user=self.user1)

        first_number_of_mail = len(mail.outbox)
        response = self.client.delete(url)
        if len(self.data['members']) > settings.NUMBER_OF_MEMBERS[self.data['event']][0] - 1:
            django_rq.get_worker().work(burst=True)
            self.assertEqual(len(mail.outbox), first_number_of_mail + len(self.data['members']) + 1)
        else:
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


@override_settings(ENTRY_START_DATE=datetime.now()-timedelta(days=3), DRAWING_LOTS_DATE=datetime.now()+timedelta(days=3), ENTRY_DEADLINE_DATE=datetime.now()+timedelta(days=10))
class DrawingLotsTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email='hogehoge@example.com')
        self.user2 = User.objects.create(username='user2', email='fugafuga@example.com')
        self.url_team_list = reverse('api:team-list')
        self.events = [event[0] for event in Team.EVENT_CHOICES]

    def test_drawing_lots(self):
        self.client.force_authenticate(user=self.user1)

        event = random.choice(self.events)

        for i in range(settings.NUMBER_OF_WINNER_TEAMS[event]):
            data = create_valid_team_data(event)
            self.client.post(self.url_team_list, data, format='json')

        self.assertEqual(Team.objects.filter(event=event, is_registered=True).count(), settings.NUMBER_OF_WINNER_TEAMS[event])
        draw_lots()
        self.assertEqual(Team.objects.filter(event=event, is_registered=True).count(), settings.NUMBER_OF_WINNER_TEAMS[event])

        for i in range(10):
            data = create_valid_team_data(event)
            self.client.post(self.url_team_list, data, format='json')

        draw_lots()
        self.assertEqual(Team.objects.filter(event=event, is_registered=True).count(), settings.NUMBER_OF_WINNER_TEAMS[event])
        self.assertEqual(Team.objects.filter(event=event, is_registered=False).count(), 10)
        draw_lots()
        self.assertEqual(Team.objects.filter(event=event, is_registered=True).count(), settings.NUMBER_OF_WINNER_TEAMS[event])
        self.assertEqual(Team.objects.filter(event=event, is_registered=False).count(), 10)
