from django.urls import path
from orders.views import ProcessOrderView

urlpatterns = [
    path("new/robot-order/", ProcessOrderView.as_view(), name="process_order"),
]