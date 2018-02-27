from django.db import models

ENTITY_CONTENT_TYPES = models.Q(model__in=('person', 'movie'))
