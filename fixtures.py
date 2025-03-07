import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "KudosApi.settings")
django.setup()
from kudos_app.models import *
from django.db import transaction

@transaction.atomic
def create_users():
    org1 = Organization.objects.create(name="Tech Corp")
    org2 = Organization.objects.create(name="Biz Inc")

    for i in range(1,20):
        try:
            user = User.objects.create_user(username=f"user{i}", password="password123")
        except:
            print("User Already Exists")
        org = org1 if i % 2 == 0 else org2
        UserProfile.objects.create(user=user, organization=org, kudos_remaining=3)

@transaction.atomic
def create_kudos():
    users = list(User.objects.all())

    for _ in range(100):
        giver = random.choice(users)
        receiver = random.choice(users)
        print(giver)
        print(giver.profile)
        profile = UserProfile.objects.get(user=giver)
        if giver != receiver and profile.kudos_remaining > 0:
            Kudos.objects.create(giver=giver, receiver=receiver, message="Great work!")

if __name__ == "__main__":
    create_users()
    create_kudos()
    print("Test data created!")
