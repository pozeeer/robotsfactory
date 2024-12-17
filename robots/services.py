import datetime
import os

from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.conf import settings
from django.utils.timezone import now
from openpyxl import Workbook
from datetime import timedelta

from robots.models import Robot


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


class ExcelReportGenerator:
    """
    Класс для генерации Excel-отчетов по производству роботов.
    """

    def __init__(self):
        self.workbook = Workbook()
        self.reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
        self.file_name = "robot_report.xlsx"
        self.file_path = os.path.join(self.reports_dir, self.file_name)

    def get_last_week_data(self):
        """
        Выбирает данные о роботах за последнюю неделю.
        """
        current_date = now()
        last_week_date = current_date - timedelta(days=7)
        robots = Robot.objects.filter(created__gte=last_week_date)

        if not robots.exists():
            raise ValueError("Нет данных для формирования отчета.")

        return robots

    def group_data_by_model(self, robots):
        """
        Группирует данные по моделям и версиям.
        """
        grouped_data = {}
        models = robots.values("model").distinct()

        for model in models:
            versions = (
                robots.filter(model=model["model"])
                .values("version")
                .annotate(count=Count("id"))
            )
            grouped_data[model["model"]] = list(versions)

        return grouped_data

    def create_sheets(self, grouped_data):
        """
        Создает страницы в Excel-файле для каждой модели.
        """
        for model, versions in grouped_data.items():
            sheet = self.workbook.create_sheet(title=model)
            sheet.append(["Модель", "Версия", "Количество за неделю"])

            for version in versions:
                sheet.append([model, version["version"], version["count"]])

        # Удаляем стандартный пустой лист
        if "Sheet" in self.workbook.sheetnames:
            self.workbook.remove(self.workbook["Sheet"])

    def save_to_file(self):
        """
        Сохраняет файл в файловую систему.
        """
        os.makedirs(self.reports_dir, exist_ok=True)
        self.workbook.save(self.file_path)

    def generate_report(self):
        """
        Основной метод для генерации отчета.
        """
        try:
            robots = self.get_last_week_data()
            grouped_data = self.group_data_by_model(robots)
            self.create_sheets(grouped_data)
            self.save_to_file()
            return os.path.join(settings.MEDIA_URL, "reports", self.file_name)
        except ValueError as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Ошибка при генерации отчета: {str(e)}")
