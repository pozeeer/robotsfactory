from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from robots.models import Robot
from django.core.exceptions import ValidationError


class RobotService:
    @staticmethod
    def create_robot(data):
        """
        Обрабатывает данные, создает запись в базе и возвращает объект.
        """
        model = data.get("model")
        version = data.get("version")
        created = parse_datetime(data.get("created"))

        if not model or not version or not created:
            raise ValidationError("Invalid data format")

        created = make_aware(created)
        robot = Robot.objects.create(model=model, version=version, created=created)
        return robot
