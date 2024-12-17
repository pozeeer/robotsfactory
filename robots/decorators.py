from functools import wraps
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError


def catch_exceptions(func):
    @wraps(func)
    def wrapper(view_instance, request, *args, **kwargs):
        try:
            return func(view_instance, request, *args, **kwargs)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValidationError:
            return JsonResponse({"error": "Validation Error"}, status=400)
        except TypeError:
            return JsonResponse({"error": "Type Error"}, status=400)
        except ValueError:
            return JsonResponse({"error": "Value Error"}, status=400)

    return wrapper

def handle_report_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            # Если данных нет для отчета
            return JsonResponse({"error": "Нет данных для формирования отчета."}, status=404)
        except Exception:
            # Любая другая ошибка
            return JsonResponse({"error": "Не удалось сформировать отчет. Обратитесь к администратору."}, status=500)
    return wrapper