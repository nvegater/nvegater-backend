from django.db import models


class Stock(models.Model):
    stock_name = models.CharField(max_length=30)

    def __str__(self):
        return self.stock_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=30)
    reporter = models.ForeignKey(Stock, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient_name
