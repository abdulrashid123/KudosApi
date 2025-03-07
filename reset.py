import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KudosApi.settings")
django.setup()
from django.db import transaction
from kudos_app.models import UserProfile

@transaction.atomic
def reset_user_kudos():
    UserProfile.objects.all().update(kudos_remaining=3)


if __name__ == "__main__":
    reset_user_kudos()
    print("Reset Kudos!")