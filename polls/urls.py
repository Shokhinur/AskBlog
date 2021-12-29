from django.urls import path, include
from .views import PollViewSet, SendCode
# from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('polls', PollViewSet, 'polls')
#
#
# urlpatterns = [
#     path('', include(router.urls)),
#
# ]
from django.urls import path
from . import views
urlpatterns = [
    path('', PollViewSet.as_view()),
    path('resetpass/', SendCode.as_view())
]



