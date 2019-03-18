from django.conf.urls import url
from .views import StatusAPIView, StatusDetailAPIView  # StatusCreateAPIView, StatusUpdateAPIView, StatusDeleteAPIView

urlpatterns = [
    url(r'^$', StatusAPIView.as_view()),
    url(r'^(?P<id>\d+)/$', StatusDetailAPIView.as_view(), name='detail'),
    # url(r'^create/$', StatusCreateAPIView.as_view()),
    # url(r'^(?P<pk>\d+)/update/$', StatusUpdateAPIView.as_view()),
    # url(r'^(?P<pk>\d+)/delete/$', StatusDeleteAPIView.as_view()),
]


# 1

# /api/status/ --> List
# /api/status/create --> Create
# /api/status/4/ --> Detail
# /api/status/4/update/ --> Update
# /api/status/4/delete/ --> Delete

# 2

# /api/status/ --> List --> CRUD
# /api/status/4/ --> Detail --> CRUD

# 3

# /api/status/ --> CRUD & LS
