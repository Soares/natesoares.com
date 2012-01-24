from django.db import models

class QuerySet(models.query.QuerySet):
    def empty(self):
        return not bool(self[:1].count())

    def not_empty(self):
        return not self.empty()


class Manager(models.Manager):
    def get_query_set(self):
        return QuerySet(self.model)

    def not_empty(self):
        return self.get_query_set().not_empty()

    def empty(self):
        return self.get_query_set().empty()
