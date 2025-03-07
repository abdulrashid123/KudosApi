from rest_framework import serializers
from kudos_app.models import Kudos, UserProfile

# Serializer for UserProfile model
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Includes all fields

    # Customize the representation to include organization name and username
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['organization'] = instance.organization.name  # Convert organization to string name
        data['username'] = instance.user.username  # Add username field
        return data

# Serializer for Kudos model
class KudosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kudos
        fields = '__all__'  # Includes all fields

    # Customize the representation to include giver and receiver usernames
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['giver_user'] = instance.giver.username  # Show giver's username
        data['receiver_user'] = instance.receiver.username  # Show receiver's username
        data['timestamp'] = instance.timestamp.date()  # Format timestamp as a date
        return data
