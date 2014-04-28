from django.db import models
from django.contrib.auth import models as auth_models


class Term(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(auth_models.User, null=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)