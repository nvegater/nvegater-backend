from django.db import models


class Stock(models.Model):
    stock_name = models.TextField()
