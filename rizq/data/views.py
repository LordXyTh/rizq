from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View

from rizq.data.tasks import update_stock_symbols


class UpdateStockDataView(View):
    def get(self, request, *args, **kwargs):
        update_stock_symbols.apply_async()
        return HttpResponseRedirect(reverse_lazy("investing:stock-index"))
