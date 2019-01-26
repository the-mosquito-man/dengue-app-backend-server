from django.core.management.base import BaseCommand, CommandError

from hospital import load


class Command(BaseCommand):
    help = 'Initial Hospital Data'

    def handle(self, *args, **options):
        load.run('data/tainan_hospital.tsv')
