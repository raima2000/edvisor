from django.template.defaultfilters import default

from elearningplatform.settings import BASE_DIR
from django.core import management
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load all fixtures automatically from all apps"

    def handle(self, *args, **options):
        fixtures = [
            'user_data.json',
            'user_data.json',
            'lecturer_data.json',
            'major_data.json',
            'course_data.json',
            'schedule_data.json',
            'class_data.json',
            'student_data.json',
            'class_announcement_data.json',
            'general_announcement_data.json',
            'class_content_data.json',
        ]

        management.call_command('makemigrations')
        management.call_command('migrate')
        for fixture in fixtures:
            print(fixture)
            management.call_command('loaddata', fixture)
