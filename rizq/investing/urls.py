from django.urls import path

from rizq.investing.views import CalculateSharesView
from rizq.investing.views import IndexStockListView
from rizq.investing.views import chart_request

app_name = "investing"

urlpatterns = [
    path("", IndexStockListView.as_view(), name="stock-index"),
    path("calculate-shares/", CalculateSharesView.as_view(), name="calculate_shares"),
    path("chart-request/", chart_request, name="chart_request"),
]
