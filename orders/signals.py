from django.db.models.signals import post_save
from django.dispatch import receiver
from robots.models import Robot
from orders.models import Order
from .services import EmailNotificationService


@receiver(post_save, sender=Robot)
def notify_customers_when_robot_available(sender, instance, created, **kwargs):
    """
    Уведомляет клиентов, если робот появился в наличии.
    """
    try:
        robot_serial = instance.serial
        order = Order.objects.filter(robot_serial=robot_serial).first()
        if order is not None:
            # Отправляем письмо клиенту
            EmailNotificationService.send_robot_available_email(
                customer_email=order.customer.email,
                robot_model=instance.model,
                robot_version=instance.version
            )
            order.delete()
    except Exception as e:
        print(f"Ошибка в функции удаления заказа и отправки пользователю письма,ошибка:{e}")
