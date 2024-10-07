from django.urls import path

from rizq.data.views import UpdateStockDataView

app_name = "data"

urlpatterns = [
    path("schedule-task/", UpdateStockDataView.as_view(), name="schedule_task"),
]
