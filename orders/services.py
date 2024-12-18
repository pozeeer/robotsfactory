import random
from time import sleep

from typing import List, Dict, Any, Optional, Union, Tuple
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail

from customers.models import Customer
from orders.models import Order
from orders.variables import GREETINGS, ROBOT_TEXT, CLOSING_TEXT
from robots.models import Robot


class EmailNotificationService:
    @staticmethod
    def send_robot_available_email(customer_email: str, robot_model: str, robot_version: str) -> None:
        """
        Отправляет email клиенту о доступности робота.

        :param customer_email: Email клиента.
        :param robot_model: Модель робота.
        :param robot_version: Версия робота.
        """
        flag = True
        attempt = 1
        while flag:       # Цикл с попытками так как иногда письмо принимается за спам и не отправляется
            message = ''
            try:
                if attempt == 10:
                    flag = False
                subject = "Робот теперь в наличии"
                generator = EmailMessageGenerator(GREETINGS, ROBOT_TEXT, CLOSING_TEXT)
                message = generator.generate_message(robot_model, robot_version)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [customer_email]

                send_mail(subject, message, from_email, recipient_list)
                flag = False
            except Exception as e:
                print(f"Ошибка при отправке письма:{message} error:{e}")
                attempt += 1
                sleep(5)


class RobotOrderService:
    @staticmethod
    def validate_request_data(data: Dict[str, Any]) -> Union[Tuple[str, str], JsonResponse]:
        """
        Проверяет, что обязательные поля присутствуют в запросе.

        :param data: Словарь с данными из запроса.
        :return: Кортеж с моделью и версией или JsonResponse с ошибкой.
        """
        model = data.get('model')
        version = data.get('version')

        if not model or not version:
            return JsonResponse({
                "error": "Поля 'model' и 'version' обязательны."
            }, status=400)

        return model, version

    @staticmethod
    def process_robot_availability(model: str, version: str) -> Optional[JsonResponse]:
        """
        Проверяет наличие робота и обновляет его статус.

        :param model: Модель робота.
        :param version: Версия робота.
        :return: JsonResponse с подтверждением или None, если робота нет.
        """
        robot = Robot.objects.filter(model=model, version=version, status='available').first()

        if robot is not None:
            robot.status = "sold"
            robot.save()  # Сохраняем обновление статуса
            return JsonResponse({
                "message": f"Робот {model}-{version} в наличии. Вы можете забрать его в ближайшем пункте выдачи."
            }, status=200)

        return None

    @staticmethod
    def create_order_if_robot_unavailable(model: str, version: str, email: Optional[str]) -> JsonResponse:
        """
        Создает заказ, если робот отсутствует.

        :param model: Модель робота.
        :param version: Версия робота.
        :param email: Email клиента.
        :return: JsonResponse с результатом обработки заказа.
        """
        if not email:
            return JsonResponse({
                "message": f"Робот {model}-{version} отсутствует. Пожалуйста, оставьте вашу почту, чтобы мы уведомили вас о его наличии."
            }, status=400)

        # Создаем или находим клиента
        customer, _ = Customer.objects.get_or_create(email=email)

        # Создаем заказ
        Order.objects.get_or_create(customer=customer, robot_serial=f"{model}-{version}")

        return JsonResponse({
            "message": f"Робот {model}-{version} отсутствует. Мы уведомим вас по почте ({email})."
        }, status=200)


class EmailMessageGenerator:
    def __init__(self, greetings: List[str], robot_text: List[str], closing_text: List[str]) -> None:
        """
        Инициализирует генератор сообщений.

        :param greetings: Список приветствий.
        :param robot_text: Список шаблонов текста про робота.
        :param closing_text: Список заключительных фраз.
        """
        self.greetings = greetings
        self.robot_text = robot_text
        self.closing_text = closing_text

    def generate_message(self, model: str, version: str) -> str:
        """
        Генерирует сообщение на основе случайных частей.

        :param model: Модель робота.
        :param version: Версия робота.
        :return: Сгенерированное сообщение.
        """
        greeting = random.choice(self.greetings)
        robot_info = random.choice(self.robot_text).format(model=model, version=version)
        closing = random.choice(self.closing_text)
        return f"{greeting}\n\n{robot_info}\n\n{closing}"
