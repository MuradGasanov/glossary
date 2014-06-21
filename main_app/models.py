from django.db import models
from django.contrib.auth import models as auth_models


class Project(models.Model):
    name = models.CharField(max_length=150)
    author = models.ForeignKey(auth_models.User, null=True)


class Term(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    author = models.ForeignKey(auth_models.User, null=True)
    project = models.ForeignKey(Project, null=True, default=None, blank=True)
    create_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)
