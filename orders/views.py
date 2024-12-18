import json

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from orders.decorators import handle_errors
from orders.services import RobotOrderService


@method_decorator(csrf_exempt, name='dispatch')
class ProcessOrderView(View):
    @handle_errors
    def post(self, request, *args, **kwargs):
        # Получаем данные из тела запроса
        data = json.loads(request.body)

        # Проверяем валидность данных
        validation_result = RobotOrderService.validate_request_data(data)
        if isinstance(validation_result, JsonResponse):
            return validation_result
        model, version = validation_result

        # Проверяем наличие робота
        availability_result = RobotOrderService.process_robot_availability(model, version)
        if availability_result:
            return availability_result

        # Создаем заказ, если робота нет
        email = data.get('email')
        return RobotOrderService.create_order_if_robot_unavailable(model, version, email)
