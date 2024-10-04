from django.urls import path

from rizq.investing.views import IndexStockListView

app_name = "investing"

urlpatterns = [
    path("", IndexStockListView.as_view(), name="stock-index"),
]
