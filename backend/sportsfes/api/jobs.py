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

from django.core.mail import send_mail as mail
from django.template.loader import get_template
from django.template import Context
import os


########### settings for taskqueue ##########
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)
logger = logging.getLogger(__name__)

"""
def scheduling_drawing_lottery():

    time = datetime(2019, 3, 14, 18, 50)
    logger.debug("now scheduling function")
    scheduler.add_job(draw_lots, "date", run_date=time, timezone="Asia/Tokyo", id="api.tasks.drawlots", jobstore='default', replace_existing=True)
    logger.debug("now after scheduler.add_job")
    scheduler.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    register_events(scheduler)

    scheduler.start()


def event_listener(event):
    if event.exception:
        print("The job crashed :(")
    else:
        print("The job worked")
        print(event.retval)
"""

########## draw lots ###########
def draw_lots():
    dictionary = {}
    for event in Team.EVENT_CHOICES:
        teams = Team.objects.filter(event=event[0])        
        team_ids = [team.pk for team in teams]

        if not teams:
            # その競技種目に出場チームがなかった場合
            winner_teams = []

        elif len(teams) <= settings.NUMBER_OF_WINNER_TEAM[event[0]]:
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

            winner_ids = np.random.choice(team_ids, size=settings.NUMBER_OF_WINNER_TEAM[event[0]], replace=False, p=data)

            for id in winner_ids:
                try:
                    team = Team.objects.get(pk=id)
                    winner_teams.append(team)
                except Team.DoesNotExist:
                    pass
                    
        dictionary[event[0]] = winner_teams

    return dictionary

def send_mail():
    winners = draw_lots()
    module_dir = os.path.dirname(__file__)
    titles = {}
    titles['winner'] = open(os.path.join(module_dir, 'templates/mail/winner/subject.txt'), 'r', encoding='utf-8').read()
    titles['loser'] = open(os.path.join(module_dir, 'templates/mail/winner/subject.txt'), 'r', encoding='utf-8').read()

    for event, winner_teams in winners.items():
        if len(winner_teams) > 0:
            all_teams = Team.objects.filter(event=event)
            for team in all_teams:
                members = team.members.all()
                for member in members:
                    if team in winner_teams:
                        mail(titles['winner'],
                                  get_template('mail/winner/body.html').render(
                                      {
                                          'member': member
                                      }
                                  ), 
                                  '{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS),
                                  ['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)],
                                  fail_silently=False
                        )
                    else:
                        mail(titles['loser'],
                                  get_template('mail/winner/body.html').render(
                                      {
                                          'member': member
                                      }
                                  ),
                                  '{from_name} <{from_address}>'.format(from_name=settings.FROM_NAME, from_address=settings.FROM_ADDRESS),
                                  ['{to_name} <{to_address}>'.format(to_name=member.name, to_address=member.email)],
                                  fail_silently=False
                        )

