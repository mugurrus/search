import hashlib
from django.db import models


class Document(models.Model):

    slug = models.CharField(max_length=256, unique=True)
    title = models.CharField(max_length=2048, blank=True)
    url = models.URLField(max_length=2048)
    indexed = models.BooleanField(default=False)
    index_time = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.slug
