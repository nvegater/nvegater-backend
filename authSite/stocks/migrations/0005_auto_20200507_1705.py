# Generated by Django 3.0.6 on 2020-05-07 14:05

import datetime
from django.db import migrations, models
import django.db.models.deletion
import stocks.models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_auto_20200507_1340'),
    ]

    operations = [
        migrations.CreateModel(
            name='IngredientPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='source',
            name='natural_ingredient',
        ),
        migrations.RenameField(
            model_name='price',
            old_name='price_unit',
            new_name='unit',
        ),
        migrations.RemoveField(
            model_name='category',
            name='source_id',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='price_id',
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='source_id',
        ),
        migrations.AddField(
            model_name='category',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='category_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.Category'),
        ),
        migrations.AddField(
            model_name='price',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='price',
            name='incoterm',
            field=models.CharField(choices=[(stocks.models.Incoterms['EXW'], 'EXW'), (stocks.models.Incoterms['FCA'], 'FCA'), (stocks.models.Incoterms['DDP'], 'DDP')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='packaging',
            field=models.CharField(choices=[(stocks.models.Packaging['BULK'], 'Bulk')], max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='prime_cost',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='price',
            name='prime_cost_currency',
            field=models.CharField(choices=[(stocks.models.Currencies['USD'], 'USD'), (stocks.models.Currencies['EUR'], 'EUR'), (stocks.models.Currencies['PLN'], 'PLN')], default=stocks.models.Currencies['PLN'], max_length=30),
        ),
        migrations.AddField(
            model_name='provider',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_flat',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='price_per_unit',
            field=models.FloatField(null=True),
        ),
        migrations.DeleteModel(
            name='NaturalIngredients',
        ),
        migrations.DeleteModel(
            name='Source',
        ),
        migrations.AddField(
            model_name='ingredientprice',
            name='ingredient_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.Ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientprice',
            name='price_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stocks.Price'),
        ),
    ]
