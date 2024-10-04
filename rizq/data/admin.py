from django.contrib import admin
from django.db.models import Sum

from rizq.data.models import IndexStock


@admin.register(IndexStock)
class IndexStockAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "name",
        "price",
        "market_cap",
        "active",
        "weighted_market_cap",
    )

    @admin.display(
        description="Weighted Market Cap (%)",
    )
    def weighted_market_cap(self, obj):
        total_market_cap = IndexStock.objects.aggregate(total=Sum("market_cap"))["total"]
        if total_market_cap and obj.market_cap:
            weighted_value = (obj.market_cap / total_market_cap) * 100
            return round(weighted_value, 2)  # Rounding to two decimal places
        return 0

    # Make it read-only (no editing)
    readonly_fields = ["weighted_market_cap"]
    list_filter = ("active",)
    search_fields = ("symbol",)
    ordering = ("-market_cap",)
