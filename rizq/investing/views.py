from django.db.models import Sum
from django.views.generic import ListView

from rizq.data.models import IndexStock
from rizq.investing.utils.weighted_marketcap import calculate_weighted_market_cap


class IndexStockListView(ListView):
    queryset = IndexStock.objects.filter(active=True)
    template_name = "investing/index_stock_list.html"
    context_object_name = "stocks"
    ordering = ["-market_cap"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_market_cap = IndexStock.objects.aggregate(total=Sum("market_cap"))["total"]
        for stock in context["stocks"]:
            stock.weighted_market_cap = calculate_weighted_market_cap(stock.market_cap, total_market_cap)
        return context
