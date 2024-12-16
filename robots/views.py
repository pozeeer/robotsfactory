import json

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from robots.decorators import catch_exceptions
from robots.services import RobotService


@method_decorator(csrf_exempt, name='dispatch')
class RobotCreateView(View):

    @catch_exceptions
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        robot = RobotService.create_robot(data)
        return JsonResponse({"message": "Robot created successfully", "id": robot.id}, status=201)
