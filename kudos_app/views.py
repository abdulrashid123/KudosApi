from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import status
from kudos_app.serializers import *
from kudos_app.models import *
from django.db import transaction

# API view for verifying JWT tokens and generating a new access token
class VerifyView(APIView):
    def get(self, request):
        user = request.user  # Get the authenticated user
        refresh = RefreshToken.for_user(user)  # Generate refresh token
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        return Response(data, status=status.HTTP_200_OK)

# API view to fetch user profile information
class UserProfileView(APIView):

    def get(self, request, single=None):
        user = request.user
        profile = user.profile  # Get user profile
        organization = profile.organization  # Get user's organization

        if single:  # If `single` is passed, return only the user's profile
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Fetch all profiles in the same organization except the current user
        profile = UserProfile.objects.filter(organization=organization).exclude(user=user)
        serializer = UserProfileSerializer(profile, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API view to handle Kudos retrieval and creation
class KudosView(APIView):

    def get(self, request):
        # Retrieve all Kudos received by the authenticated user
        user = request.user
        objs = Kudos.objects.filter(receiver=user)
        serializer = KudosSerializer(objs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic  # Ensure atomic transaction
    def post(self, request):
        # Process kudos giving functionality
        data = request.data
        user = request.user
        profile = user.profile

        if profile.kudos_remaining > 0:  # Ensure user has remaining kudos
            serializer = KudosSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # Refresh the user profile data after giving kudos
                profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(profile)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Kudos Not remaining"}, status.HTTP_400_BAD_REQUEST)
