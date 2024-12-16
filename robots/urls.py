from django.urls import path

from robots.views import RobotCreateView

urlpatterns = [
    path('create/new_robot/',RobotCreateView.as_view(),name='create-new-robot')
]