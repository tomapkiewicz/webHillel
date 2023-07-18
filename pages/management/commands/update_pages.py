from django.core.management.base import BaseCommand
from django.utils import timezone
from pages.models import Page
from datetime import datetime
import pytz


class Command(BaseCommand):
    help = "Updates the activa field for pages where fecha is before today"

    def handle(self, *args, **options):
        local_tz = pytz.timezone("America/Argentina/Buenos_Aires")
        today = datetime.now(local_tz).date()
        pages_to_update = Page.objects.filter(fecha__lt=today, activa=True)
        pages_to_update.update(activa=False)
        self.stdout.write(self.style.SUCCESS("Successfully updated pages."))
