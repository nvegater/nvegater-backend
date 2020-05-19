import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from .models import Country


# Create a GraphQL type for the Countrymodel
class CountryType(DjangoObjectType):
    class Meta:
        model = Country


class Query(ObjectType):
    country = graphene.Field(CountryType, id=graphene.Int())
    countries = graphene.List(CountryType)

    @staticmethod
    def resolve_country(info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Country.objects.get(pk=id)
        return None

    @staticmethod
    def resolve_movies(info, **kwargs):
        return Country.objects.all()
