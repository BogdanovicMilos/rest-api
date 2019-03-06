from django.conf.urls import url
from .views import UpdateModelDetailAPIView, UpdateModelListAPIView, UpdateListView, UpdateDetailView

urlpatterns = [
    url(r'^$', UpdateModelListAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', UpdateModelDetailAPIView.as_view()),
    url(r'^list/$', UpdateListView.as_view()),
    url(r'^list/(?P<id>\d+)/$', UpdateDetailView.as_view())
]
