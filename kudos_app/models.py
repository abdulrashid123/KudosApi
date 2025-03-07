from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Model representing an organization
class Organization(models.Model):
    name = models.CharField(max_length=255)  # Organization name
    last_reset = models.DateField(auto_now_add=True)  # Stores the last reset date

    def __str__(self):
        return self.name

# Model representing a user profile associated with an organization
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")  # Link to Django User model
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='user_organization')  # Organization the user belongs to
    kudos_remaining = models.IntegerField(default=3)  # Number of kudos a user can give (resets weekly)
    kudos_gain = models.IntegerField(default=0)  # Number of kudos received by the user

# Model representing a Kudos (peer appreciation)
class Kudos(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kudos_given")  # User giving kudos
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="kudos_received")  # User receiving kudos
    message = models.TextField()  # Message attached to kudos
    timestamp = models.DateTimeField(default=timezone.now)  # Time when kudos was given

    def __str__(self):
        return f"{self.giver} -> {self.receiver}: {self.message}"


# Signal to update user profile stats when a Kudos instance is created
@receiver(post_save, sender=Kudos)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        print(instance.receiver, instance, instance.giver)
        # Deduct one kudos from the giver
        giver_profile = UserProfile.objects.get(user=instance.giver)
        giver_profile.kudos_remaining -= 1
        giver_profile.save()
        # Increment the kudos count for the receiver
        receiver_profile = UserProfile.objects.get(user=instance.receiver)
        receiver_profile.kudos_gain += 1
        receiver_profile.save()
