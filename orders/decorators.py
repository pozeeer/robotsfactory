from functools import wraps
from django.http import JsonResponse
import json

from robots.models import Robot


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Неверный формат JSON."}, status=400)
        except Robot.DoesNotExist:
            return JsonResponse({"error": "Указанный робот не найден."}, status=404)
        except Exception as e:
            return JsonResponse({"error": "Внутренняя ошибка сервера."}, status=500)
    return wrapper
