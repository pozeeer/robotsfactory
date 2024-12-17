from django.urls import path

from robots.views import RobotCreateView, ExcelReportView

urlpatterns = [
    path('create/new_robot/', RobotCreateView.as_view(), name='create-new-robot'),
    path("excel/week/report/", ExcelReportView.as_view(), name="week_report"),
]
