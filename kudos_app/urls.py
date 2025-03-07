from django.urls import path
from kudos_app.views import *
urlpatterns = [
    path('verify-user/',VerifyView.as_view()),
    path('get-user-profile/<str:single>/',UserProfileView.as_view()),
    path('get-user-profile/',UserProfileView.as_view()),
    path('get-user-kudos/',KudosView.as_view()),
    path('create-kudos/',KudosView.as_view())
]