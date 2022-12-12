import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    UserCustomized
)

TABLES = {
    UserCustomized: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
}


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        for model, csv_file in TABLES.items():
            with open(
                f'{settings.BASE_DIR}/static/data/{csv_file}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Данные загружены'))
