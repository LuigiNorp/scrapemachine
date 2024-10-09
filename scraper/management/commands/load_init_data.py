import json
import logging
from django.core.management.base import BaseCommand
from scraper.models import Website

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Custom Django command to populate the Website model with initial data.
    """
    help = 'Populate the Website model with initial data'

    def handle(self, *args, **kwargs):
        """
        Reads a JSON file with initial data and inserts it into the Website model.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Raises:
            FileNotFoundError: If the JSON file is not found.
        """
        try:
            with open('scraper/management/commands/initial_data.json') as f:
                data = json.load(f)
                for item in data:
                    fields = item['fields']
                    if not Website.objects.filter(site_name=fields['site_name'], url=fields['url']).exists():
                        Website.objects.create(**fields)
                        self.stdout.write(self.style.SUCCESS(f"Successfully added {fields['site_name']}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"{fields['site_name']} already exists"))
            self.stdout.write(self.style.SUCCESS('Finished populating the Website model'))
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            self.stdout.write(self.style.ERROR('Failed to populate the Website model: initial data file not found'))
