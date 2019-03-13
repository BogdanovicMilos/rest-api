from django.conf.urls import url
from .views import AuthAPIView, RegisterAPIView
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    url(r'^$', AuthAPIView.as_view()),
    url(r'^register/$', RegisterAPIView.as_view()),
    url(r'^jwt/$', obtain_jwt_token),
    url(r'^jwt/refresh/$', refresh_jwt_token),
]
