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
