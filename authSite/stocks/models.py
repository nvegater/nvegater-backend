from django.db import models
from datetime import datetime
from enum import Enum


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
    date_created = models.DateTimeField(default=datetime.now)
    stock_name = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.stock_name


class Country(models.Model):
    country_name = models.CharField(max_length=30, null=False, unique=True, default="unknown")


class NaturalIngredients(models.Model):
    ingredient_name = models.CharField(max_length=30, null=False)


class Source(models.Model):
    source_name = models.CharField(max_length=30)
    natural_ingredient = models.ForeignKey(NaturalIngredients, on_delete=models.CASCADE)


class Category(models.Model):
    category_name = models.CharField(max_length=30, null=False, unique=True)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)
    categoryType = models.CharField(max_length=30, choices=[(tag, tag.value) for tag in Categories], null=False)
    protein_content = models.CharField(max_length=30, null=True)
    production_type = models.CharField(max_length=30, null=True)
    fat_content = models.CharField(max_length=30, null=True)
    additives = models.CharField(max_length=30, null=True)
    soluble = models.BooleanField(null=True)
    liquid = models.BooleanField(null=True)
    powder = models.BooleanField(null=True)
    roasted = models.BooleanField(null=True)
    fineness = models.CharField(max_length=30, null=True)
    natural = models.BooleanField(null=True)
    process_type = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)


class Price(models.Model):
    price_flat = models.DecimalField(max_digits=30, decimal_places=15)
    price_currency = models.CharField(max_length=30, choices=[(tag, tag.value) for tag in Currencies], null=False)
    price_unit = models.CharField(max_length=30, choices=[(tag, tag.value) for tag in Units], null=False)
    price_per_unit = models.DecimalField(max_digits=30, decimal_places=15)


class Provider(models.Model):
    provider_name = models.CharField(max_length=30, null=False)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    sold = models.BooleanField(null=True)
    provider_type = models.CharField(max_length=30, choices=[(tag, tag.value) for tag in ProviderType], null=False)
    # b = Provider(provider_name='X', provider_type=ProviderType.PROD)
    contact_name = models.CharField(max_length=30, null=False)
    email = models.CharField(max_length=30, null=False)
    website = models.CharField(max_length=30, null=False)
    phone_number = models.CharField(max_length=30, null=False)
    address = models.CharField(max_length=30, null=False)


class Ingredient(models.Model):
    date_created = models.DateTimeField(default=datetime.now)
    ingredient_name = models.CharField(max_length=30, null=False, unique=True)
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True)
    source_id = models.ForeignKey(Source, on_delete=models.CASCADE, null=True)
    price_id = models.ForeignKey(Price, on_delete=models.CASCADE, null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    ingredient_shelf_life_months = models.IntegerField(null=True)

    def __str__(self):
        return self.ingredient_name
