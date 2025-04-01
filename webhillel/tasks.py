from profiles.models import send_html_mail  # Import your existing email function
import datetime
from profiles.models import Profile
from django.template.loader import render_to_string  # Import this
 

def send_birthday_emails():
    """Sends a birthday email to users with a birthday today."""
    today = datetime.date.today()
    
    birthday_users = Profile.objects.filter(
        fechaNacimiento__month=today.month,
        fechaNacimiento__day=today.day,
        user__email__isnull=False  # Ensure the user has an email
    )

    sent_count = 0
    for profile in birthday_users:
        user = profile.user  # Get the related User

        subject = f"¡Feliz cumpleaños, {profile.nombre or user.username}!"
        html_message = loader.render_to_string(
            "birthday_email.html",  # Create this template in your app
            {
                "user_name": profile.nombre or user.username,
                "birthday_message": "🎉 ¡Esperamos que tengas un día increíble! 🎂",
            },
        )

        send_html_mail(subject, html_message, [user.email], "Hillel Argentina")
        sent_count += 1

    return f"{sent_count} birthday emails sent."