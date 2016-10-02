# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.widgets import CKEditorWidget

# Create your models here.

class SearchLabelKeeper(models.Model):
    def __str__(self):
        return self.searchlabelkeeper_marker
    class Meta():
        db_table = 'searchlabelkeeper'
    searchlabelkeeper_marker = models.CharField(max_length=200, verbose_name='Поисковая метка', unique=True)

class Keeper(models.Model):
    def __str__(self):
        return self.keep_title
    class Meta():
        db_table = 'keep'

    keep_title = models.CharField(max_length=200, verbose_name='Название статьи')
    # keep_text = models.TextField(verbose_name='Текст статьи')
    keep_text = RichTextUploadingField(verbose_name='Текст статьи')
    keep_data = models.DateTimeField(null=True)
    keep_hashTag = models.ManyToManyField(SearchLabelKeeper)


class Feedback(models.Model):
    def __str__(self):
        return self.feedback_text
    class Meta():
        db_table = 'feedback'

    feedback_text = models.TextField(verbose_name='Комментарий') #verbose_name - читаемое поле
    feedback_data = models.DateTimeField(null=True)
    feedback_keeper = models.ForeignKey(Keeper)
    feedback_from = models.ForeignKey(User)

class Suggestions(models.Model):
    def __str__(self):
        return self.suggestions_text
    class Meta():
        db_table = 'suggestions'

    suggestions_text = models.TextField(verbose_name='Исправления') #verbose_name - читаемое поле
    suggestions_data = models.DateTimeField(null=True)
    suggestions_keeper = models.ForeignKey(Keeper)
    suggestions_from = models.ForeignKey(User)



class KeeperStatus(models.Model):
    def __str__(self):
        return self.keeper_status_text
    class Meta():
        db_table = 'keeperstatus'

    keeper_status_text = models.CharField(max_length=100, verbose_name='Статус статьи')