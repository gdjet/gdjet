from django.db import models

class EmptyQ(models.Q):
    """
        Just to identify an Empty Q Object.
    """
    pass

class Q(models.Q):
    """
        Q Object which combined with an EmptyQ Object does literally nothing.
    """
    def _combine(self, other, conn):
        if isinstance(other, EmptyQ):
            return self
        return models.Q._combine( self, other, conn )

