from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class QuestionManager(models.Manager):
    def new(self):
        return self.get_queryset().all().order_by('-id')

    def popular(self):
        return self.get_queryset().all().order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, related_name='author')
    likes = models.ManyToManyField(User, related_name='liked', blank=True)
    objects = QuestionManager()

    def get_url(self):
        return reverse('question',kwargs={'pk': self.pk})


class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateField(auto_now_add=True)
    question = models.ForeignKey(Question)
    author = models.ForeignKey(User)

    def get_url(self):
        return reverse('question', kwargs={'pk': self.question_id})
