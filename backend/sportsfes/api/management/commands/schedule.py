from django.core.management.base import BaseCommand, CommandError
from api import jobs
import time
import threading
import sys


class Command(BaseCommand):
    help = "Schedule pulling lots for sports festival"

    def handle(self, *args, **options):
        jobs.schedule_drawing_lottery()
        self.stdout.write(self.style.SUCCESS('Successfully scheduled drawing lots'))

        while True:
            if not jobs.scheduler.get_jobs():
                self.stdout.write(self.style.SUCCESS('sent mail to members'))
                sys.exit()

            time.sleep(10)
        

