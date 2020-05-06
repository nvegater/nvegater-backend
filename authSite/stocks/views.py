from django.shortcuts import render
from django.http import HttpResponseRedirect

from stocks.models import Stock, Ingredient


def stock_all(request):
    all_stocks = Stock.objects.all()
    if not all_stocks:
        return HttpResponseRedirect("/empty-stocks/")
    all_ingredients = Ingredient.objects.all()
    if not all_ingredients:
        return HttpResponseRedirect("/empty-ingredients/")
    return render(request, {'stocks': all_stocks, 'ingredients': all_ingredients})
