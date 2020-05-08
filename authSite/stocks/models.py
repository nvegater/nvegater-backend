from django.db import models
from datetime import datetime
from enum import Enum
import uuid


class ProviderType(Enum):
    PROD = "Producer"
    SUPP = "Supplier"
    PROD_SUPP = "Producer and Supplier"


class Currencies(Enum):
    USD = "USD"
    EUR = "EUR"
    PLN = "PLN"


class Units(Enum):
    KG = "KG"
    LB = "LB"
    MT = "MT"
    LT = "LT"


class Categories(Enum):
    PROTEIN = "Protein"
    MILK_SUBSTITUTE = "Milk Substitute"
    PASTE = "Paste"
    SWEETENER = "Sweetener"
    OIL = "Oil"
    FRUIT = "Fruit"


class Stock(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(default=datetime.now)
    stock_name = models.CharField(max_length=60, null=False, unique=True)

    def __str__(self):
        return self.stock_name


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country_name = models.CharField(max_length=60, null=False, unique=True)


class Provider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #  Provider comes from only one country.
    date_created = models.DateTimeField(default=datetime.now)
    provider_name = models.CharField(max_length=60, null=False, unique=False)
    country_id = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    sold = models.BooleanField(null=True)
    provider_type = models.CharField(max_length=60, choices=[(tag, tag.value) for tag in ProviderType], null=False)
    # b = Provider(provider_name='X', provider_type=ProviderType.PROD)
    contact_name = models.CharField(max_length=60, null=False)
    email = models.CharField(max_length=60, null=False)
    website = models.CharField(max_length=60, null=False)
    phone_number = models.CharField(max_length=60, null=False)
    address = models.CharField(max_length=60, null=False)


# You want to be able to identify when a cheaper ingredient is offered. (in one category)
# Provider 1 offers Ingredient X from Category A in Price N
# Ira checks prices of Ingredients from Category A and finds Ingredient Y (similar to X) in Price M

# Price N > Price M : No thank you, too expensive
# Price N < Price M : Cool, cheap ingredient


# you want to be able to negotiate prices with providers and registrate negotiations
# Provider 1 offers Ingredient X from Category A in Price N
# Ira checks prices of Ingredients from Category A and finds Ingredient Y in Price M
# Price N > Price M : No thank you, too expensive
# Provider 1 offers Ingredient X from Category A in Price P
# Ingredient X has now 2 prices. Is possible to register changes for ingredient X
# Price P < Price M : Cool, cheap ingredient!!

# Ira buys more of that ingredient, for different prices. Ingredient X has multiple prices.

# you want to receive alerts when the same price was given to another ingredient.
# this can create some intuition and comparison of how much an ingredients actually costs.

# Same Reasoning but with nutritional value

class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(default=datetime.now)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    # an unique ingredient that comes from ONLY one: provider, country. Belongs to ONLY one category
    ingredient_name = models.CharField(max_length=60, null=False, unique=True)
    category_type = models.CharField(max_length=60, choices=[(tag, tag.value) for tag in Categories], null=False)
    country_id = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    ingredient_shelf_life_months = models.IntegerField(null=True)

    def __str__(self):
        return self.ingredient_name


# Same nutritional Value can belong to many ingredients
class NutrionalValue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    protein_content = models.CharField(max_length=60, null=True)
    production_type = models.CharField(max_length=60, null=True)
    fat_content = models.CharField(max_length=60, null=True)
    additives = models.CharField(max_length=60, null=True)
    soluble = models.BooleanField(null=True)
    liquid = models.BooleanField(null=True)
    powder = models.BooleanField(null=True)
    roasted = models.BooleanField(null=True)
    natural = models.BooleanField(null=True)
    state = models.CharField(max_length=60, null=True)
    fineness = models.CharField(max_length=60, null=True)
    process_type = models.CharField(max_length=60, null=True)


class Price(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(default=datetime.now)
    price_flat = models.FloatField(null=True)
    price_currency = models.CharField(max_length=60, choices=[(tag, tag.value) for tag in Currencies], null=False)
    unit = models.CharField(max_length=60, choices=[(tag, tag.value) for tag in Units], null=False)
    price_per_unit = models.FloatField(null=True)
    incoterm = models.CharField(max_length=60, null=True)
    packaging = models.CharField(max_length=60, null=True)
    prime_cost = models.FloatField(null=True)
    prime_cost_currency = models.CharField(max_length=60, choices=[(tag, tag.value) for tag in Currencies], null=False,
                                           default=Currencies.PLN)
