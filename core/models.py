import uuid

from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import connection, models
from django.urls import reverse  # updated import for Django 3.x


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=36, blank=True, default=uuid.uuid4)
    weekly = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Problem(models.Model):
    title = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    slug = models.SlugField(unique=True)
    date = models.DateField(unique=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.title + "-" + str(self.date)

    def get_absolute_url(self):
        return reverse("core.views.problem", args=[self.slug])


class ProblemSuggestion(models.Model):
    text = models.TextField()
    problem = models.ForeignKey(
        Problem, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    path = ArrayField(models.IntegerField(), null=True)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, null=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    spam = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    @property
    def indent(self):
        return (len(self.path) - 1) * 2

    def has_children(self):
        # This can be done through the ORM when 1.7 releases with path__contains
        cursor = connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM core_comment WHERE path @> %s", [self.path]
        )
        return cursor.fetchone()[0] > 1
