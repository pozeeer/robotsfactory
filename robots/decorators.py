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
    return wrapper