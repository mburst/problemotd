from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from djorm_pgarray.fields import ArrayField
import uuid


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=36, blank=True, default=uuid.uuid4)
    weekly = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email


class Problem(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    date = models.DateField(unique=True)

    class Meta:
        ordering=['-date']

    def __unicode__(self):
        return self.title + '-' + str(self.date)

    def get_absolute_url(self):
        return reverse('core.views.problem', args=[self.slug])


class ProblemSuggestion(models.Model):
    text = models.TextField()
    problem = models.ForeignKey(Problem, null=True)

    def __unicode__(self):
        return self.text


class Comment(models.Model):
    path = ArrayField(dbtype='int', null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem)
    user = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    spam = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

    @property
    def indent(self):
        return (len(self.path)-1)*2
