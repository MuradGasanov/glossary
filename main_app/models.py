from django.db import models


class Term(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)