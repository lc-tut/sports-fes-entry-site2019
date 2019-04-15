from .models import *
from django.conf import settings

from apscheduler.events import *
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import *
from datetime import datetime
import json
import logging
import time

from django.core.mail import send_mail as mail
from django.core.mail import EmailMessage
from django.template.loader import get_template, render_to_string
from django.template import Context
import os


########### settings for taskqueue ##########
jobstores = {
    'default': SQLAlchemyJobStore(url='postgresql+psycopg2://database1_role:database1_password@database1/database1', tablename='apscheduler_jobs')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': True,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, daemon=True)
logger = logging.getLogger(__name__)


def schedule_drawing_lottery():

    logger.debug("now scheduling function")
    scheduler.add_job(send_mail, "date", args=['draw-lots'], run_date=settings.DRAWING_LOTS_DATE, timezone="Asia/Tokyo", id="api.tasks.send_mail", replace_existing=True)
    logger.debug("now after scheduler.add_job")
    #scheduler.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    #register_events(scheduler)
    scheduler.start()



def event_listener(event):
    if event.exception:
        print("The job crashed :(")
    else:
        print("The job worked")
        scheduler.shutdown(wait=False)


########## draw lots ###########
def draw_lots():
    dictionary = {}
    for event in Team.EVENT_CHOICES:
        teams = Team.objects.filter(event=event[0])        
        team_ids = [team.pk for team in teams]

        if not teams:
            # その競技種目に出場チームがなかった場合
            winner_teams = []

        elif len(teams) <= settings.NUMBER_OF_WINNER_TEAMS[event[0]]:
            winner_teams = teams
        else:
            data = []
            for team in teams:
                members = team.members.all()
                admission_years = []
                for member in members:
                    scraped_year = int(member.email[3:5])
                    rounded_year = round(datetime.datetime.now().year, -2)
                    admission_year = rounded_year + scraped_year if rounded_year < rounded_year + scraped_year < rounded_year + 100 else rounded_year + scraped_year - 100 
                    admission_years.append(admission_year)

                average = np.mean(admission_years)
                data.append(average)

            data = np.array(data)
            data = datetime.datetime.now().year - data
            data = np.sum(data) - data
            data = data / np.sum(data) # Now, data is a list of probabilities

            winner_ids = np.random.choice(team_ids, size=settings.NUMBER_OF_WINNER_TEAMS[event[0]], replace=False, p=data)

            for id in winner_ids:
                try:
                    team = Team.objects.get(pk=id)
                    winner_teams.append(team)
                except Team.DoesNotExist:
                    pass
                    
        dictionary[event[0]] = winner_teams

    return dictionary

def send_mail(function, team=None, member_changed=None):
    module_dir = os.path.dirname(__file__)

    if function == 'team-create':
        for member in team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/team-create/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/team-create/body.html', {'member': member, 'team': team})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()
    elif function == 'team-update':
        for member in team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/team-update/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/team-update/body.html', {'member': member, 'team': team})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()        
    elif function == 'team-delete':
        for member in team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/team-delete/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/team-delete/body.html', {'member': member, 'team': team})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()       
    elif function == 'member-create':
        for member in member_changed.team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/member-create/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/member-create/body.html', {'member': member, 'member_changed': member_changed})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()
    elif function == 'member-update':
        for member in member_changed.team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/member-update/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/member-update/body.html', {'member': member, 'member_changed': member_changed})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()
    elif function == 'member-delete':
        for member in member_changed.team.members.all():
            title = open(os.path.join(module_dir, 'templates/mail/member-delete/subject.txt'), 'r', encoding='utf-8').read()
            msg_html = render_to_string('mail/member-delete/body.html', {'member': member, 'member_changed': member_changed})
            msg = EmailMessage(subject=title, body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
            msg.content_subtype = "html"
            msg.send()       
    elif function == 'draw-lots':
        winners = draw_lots()
        titles = {}
        titles['winner'] = open(os.path.join(module_dir, 'templates/mail/winner/subject.txt'), 'r', encoding='utf-8').read()
        titles['loser'] = open(os.path.join(module_dir, 'templates/mail/loser/subject.txt'), 'r', encoding='utf-8').read()

        for event, winner_teams in winners.items():
            if len(winner_teams) > 0:
                all_teams = Team.objects.filter(event=event)
                for team in all_teams:
                    members = team.members.all()
                    for member in members:
                        if team in winner_teams:
                            msg_html = render_to_string('mail/winner/body.html', {'member': member})
                            msg = EmailMessage(subject=titles['winner'], body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
                            msg.content_subtype = "html"
                            msg.send()
                            print("send message")
                        else:
                            msg_html = render_to_string('mail/loser/body.html', {'member': member})
                            msg = EmailMessage(subject=titles['loser'], body=msg_html, from_email='{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS), bcc=['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)])
                            msg.content_subtype = "html"
                            msg.send()                  