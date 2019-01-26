from django.core.management.base import BaseCommand, CommandError

from taiwan import load


class Command(BaseCommand):
    help = 'Son of bitch'

    def handle(self, *args, **options):
        load.run()
