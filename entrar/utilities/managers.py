from django.db import models
from utilities.query import QuerySet

class Manager(models.Manager):
    def get_query_set(self):
        return QuerySet(self.model)

    def not_empty(self):
        return self.get_query_set().not_empty()

    def empty(self):
        return self.get_query_set().empty()

    def first(self):
        return self.get_query_set().first()

    def last(self):
        return self.get_query_set().last()
