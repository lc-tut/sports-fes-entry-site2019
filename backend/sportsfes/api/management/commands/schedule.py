from django.core.management.base import BaseCommand, CommandError
from api import jobs
import time


class Command(BaseCommand):
    help = "Schedule pulling lots for sports festival"

    def handle(self, *args, **options):
        jobs.schedule_drawing_lottery()
        
        try:
            print("Press <Ctrl + C> to stop!")
            time.sleep(10000000)
        except KeyboardInterrupt:
            print('Stopping...')
            jobs.scheduler.shutdown()

        self.stdout.write(self.style.SUCCESS('Successfully scheduled drawing lots'))