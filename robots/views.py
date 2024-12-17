import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from robots.services import ExcelReportGenerator
from robots.decorators import catch_exceptions, handle_report_errors
from robots.services import RobotService


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):

    @catch_exceptions
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        robot = RobotService.create_robot(data)
        return JsonResponse({"message": "Robot created successfully", "id": robot.id}, status=201)


class ExcelReportView(View):
    @handle_report_errors
    def get(self, request, *args, **kwargs):
        generator = ExcelReportGenerator()
        report_url = generator.generate_report()
        return JsonResponse({"report_url": request.build_absolute_uri(report_url)})
