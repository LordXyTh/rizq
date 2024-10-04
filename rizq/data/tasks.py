from celery import shared_task
from django.utils import timezone

from rizq.data.models import IndexStock
from rizq.data.utils.fetch_market_data import fetch_market_data
from rizq.data.utils.fetch_stocks import fetch_stock_symbols


@shared_task(soft_time_limit=300, time_limit=300)
def update_stock_symbols():
    # Fetch current symbols and their data
    current_symbols_data = fetch_stock_symbols()

    # Step 1: Update or create current symbols and set active to True for existing symbols
    for symbol, data in current_symbols_data.items():
        stock, created = IndexStock.objects.update_or_create(
            symbol=symbol,
            defaults={
                "price": data["price"],
                "market_cap": data["market_cap"],
                "name": data["name"],
                "last_updated": timezone.now(),
                "active": True,
            },
        )
        # If the stock was inactive and is now being updated, activate it
        if not created and not stock.active:
            stock.active = True
            stock.save(update_fields=["active"])

    # Step 2: Deactivate symbols not in the current data
    all_symbols_in_db = set(IndexStock.objects.values_list("symbol", flat=True))
    symbols_to_deactivate = all_symbols_in_db - set(current_symbols_data.keys())
    IndexStock.objects.filter(symbol__in=symbols_to_deactivate).update(active=False)


@shared_task
def update_stock_prices():
    stocks = IndexStock.objects.filter(active=True)
    for stock in stocks:
        data = fetch_market_data(stock.symbol)
        stock.price = data["current_price"]
        stock.market_cap = data["market_cap"]
        stock.last_updated = timezone.now()
        stock.save()
