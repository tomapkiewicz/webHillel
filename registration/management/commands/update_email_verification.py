from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Updates the email_verificado field to True for all existing users."

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            try:
                if user.profile:
                    user.profile.email_verificado = True
                    user.profile.save()
            except User.profile.RelatedObjectDoesNotExist:
                pass  # If a profile doesn't exist for the user, just skip updating
        self.stdout.write(
            self.style.SUCCESS("Successfully updated email_verificado for all users.")
        )
