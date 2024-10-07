import requests
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.generic import ListView
from django.views.generic import View

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


class CalculateSharesView(View):
    def post(self, request, *args, **kwargs):
        investment_amount = float(request.POST.get("investment_amount", 0))
        stocks = IndexStock.objects.filter(active=True).order_by("-market_cap")
        total_market_cap = stocks.aggregate(total=Sum("market_cap"))["total"]

        # Create a custom list to hold stock data, including calculated attributes
        stock_data_list = []

        for stock in stocks:
            # Calculate weighted market cap
            weighted_market_cap = calculate_weighted_market_cap(stock.market_cap, total_market_cap)
            allocated_amount = (weighted_market_cap / 100) * investment_amount
            # Calculate shares to buy (no fractional shares)
            shares_to_buy = int(allocated_amount / stock.price)
            # Add stock data to the custom list
            stock_data = {
                "symbol": stock.symbol,
                "name": stock.name,
                "price": stock.price,
                "market_cap": stock.market_cap,
                "weighted_market_cap": weighted_market_cap,
                "shares_to_buy": shares_to_buy,
            }
            stock_data_list.append(stock_data)

        html = render_to_string("investing/partials/investment_suggestions.html", {"stocks": stock_data_list})
        return HttpResponse(html)


def chart_request(request):
    symbol = request.GET.get("symbol")
    url = f"https://sarmaaya.pk/ajax/widgets/company_vs_index_filter.php?symbol={symbol}&frame=yearly"
    response = requests.get(url, timeout=100)
    return HttpResponse(response.content)
