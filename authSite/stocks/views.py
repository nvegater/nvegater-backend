import csv, io, re
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from stocks.models import Stock, Ingredient, Country, NutrionalValue, Categories, Price, Currencies, Provider, \
    ProviderType


def ingredients_all(request):
    ingredients_list = serializers.serialize('json', Ingredient.objects.all(),
                                             fields=('ingredient_name', 'category_type'))
    if not ingredients_list:
        return HttpResponseRedirect("/empty-ingredients/")
    return render(request, ingredients_list)


@permission_required('admin.can_add_log_entry')  # only admin and super user
def csv_upload(request):
    template = "upload_ingredient.html"
    prompt = {
        'order':
            'Order of CSV should be: product, origin, producer/supplier, category, protein_percentage, price, Q-ty, '
            'Incoterms, price Bulk, packaging '
    }
    if request.method == "GET":
        return render(request, template, prompt)
    # grab file from the Form in case is a POST
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a CSV file')
    data_set = csv_file.read().decode('UTF-8')
    # stream in the csv file
    io_string = io.StringIO(data_set)
    # Skip first line (header)
    next(io_string)
    # TODO Maybe use serializer instead to parse file to models
    for column in csv.reader(io_string, delimiter=';'):
        # "_," Throwaway variable to save without calling save()
        new_country_name = column[2] if column[2] else 'Country name not provided'
        new_country = Country.objects.get_or_create(
            country_name=new_country_name
        )
        print("New country object created: ", new_country)

        new_provider_name = column[3] if column[3] else 'Provider name not provided'
        new_provider = Provider.objects.get_or_create(
            provider_name=new_provider_name,
            country_id=Country.objects.get(country_name=new_country_name),
            provider_type=ProviderType.PROD_SUPP
        )
        print("New provider object created: ", new_provider)
        # TODO Better enums: https://gist.github.com/treyhunner/fd2dc64efb50a147e0a29746862fe8fc
        category_type_csv = ''
        prefix_incoterm_csv = column[4][:2]
        if prefix_incoterm_csv == 'fr':
            category_type_csv = Categories.FRUIT
        if prefix_incoterm_csv == 'pl':
            category_type_csv = Categories.MILK_SUBSTITUTE
        if prefix_incoterm_csv == 'nu':
            category_type_csv = Categories.PASTE
        if prefix_incoterm_csv == 'oi':
            category_type_csv = Categories.OIL
        if prefix_incoterm_csv == 'sw':
            category_type_csv = Categories.SWEETENER
        if prefix_incoterm_csv == 'pr':
            category_type_csv = Categories.PROTEIN

        country_id_for_ingredient = Country.objects.get(country_name=new_country_name).id
        new_ingredient = Ingredient.objects.get_or_create(
            ingredient_name=column[1],
            category_type=category_type_csv,
            country_id=Country.objects.get(country_name=new_country_name),
            provider_id=Provider.objects.get(provider_name=new_provider_name, country_id=country_id_for_ingredient)
        )
        print("New ingredient object created: ", new_ingredient)

        new_nutr_value = NutrionalValue.objects.get_or_create(
            ingredient_id=Ingredient.objects.get(ingredient_name=column[1]),
            fat_content=column[5] if column[2] else '',
        )
        print("New nutritional value object created: ", new_nutr_value)

        # This column has string with other things that are not floats. correct that.
        # https://stackoverflow.com/questions/42680951/python-robustly-convert-any-string-with-units-to-float
        # More on floats https://stackoverflow.com/questions/379906/how-do-i-parse-a-string-to-a-float-or-int
        price_flat_floats = float(re.sub("[^0-9.\-]", "", column[6])) if column[6] else 0
        price_per_unit_floats = float(re.sub("[^0-9.\-]", "", column[8])) if column[8] else 0
        prime_cost_floats = float(re.sub("[^0-9.\-]", "", column[11])) if column[11] else 0

        new_price = Price.objects.get_or_create(
            price_flat=price_flat_floats,
            price_currency=column[7],
            price_per_unit=price_per_unit_floats,
            unit=column[9],
            incoterm=column[10][:3],
            prime_cost=prime_cost_floats,
            prime_cost_currency=Currencies.PLN,
            packaging=column[13]
        )
        print("New price object created: ", new_price)

    context = {}
    return render(request, template, context)
    #       COLUMNS
    # 2: Country: (country_name)
    # 5: NutrionalValue (fat_content)
    # 6: Price (price_flat)
    # 7: Price (price_currency)
    # 8: Price (price_per_unit)
    # 9: Price (unit)
    # 10: Price (incoterm) There is also origin and destination. Add them in separate columns and then update models
    # 11: Price (prime_cost)
    # 12: Price (prime_cost_currency)
    # 13: Price (packaging)
    # 1: Ingredient: (ingredient_name)
    # 4: Ingredient (category_type)
    # 3: Provider: (provider_name)
