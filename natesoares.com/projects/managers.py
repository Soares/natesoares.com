from personal.common.managers import PublishedTagManager

class ActiveManager(PublishedTagManager):
    def get_query_set(self):
        phases = 'i', 'd', 'D', 'p'
        return super(ActiveManager, self).get_query_set().filter(phase__in=phases)
