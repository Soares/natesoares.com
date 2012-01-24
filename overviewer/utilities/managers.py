from django.db import models

class QuerySet(models.query.QuerySet):
    def empty(self):
        return self.first() is None

    def not_empty(self):
        return not self.empty()

    def last(self):
        return self.reverse().first()

    def first(self):
        try:
            return self[0]
        except IndexError:
            return None


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
