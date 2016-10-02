# -*- coding: utf-8 -*-
from django.contrib import admin
import sys
import os
from keeper.models import Keeper, Feedback, Suggestions, SearchLabelKeeper, KeeperStatus

from django import forms
from ckeditor.widgets import CKEditorWidget

# Register your models here.



class FeedbackInlines(admin.StackedInline):
    model = Feedback
    extra = 1

class SuggestionsInlines(admin.StackedInline):
    model = Suggestions
    extra = 1

class KeeperAdmin(admin.ModelAdmin):
    content = forms.CharField(widget=CKEditorWidget())
    fields = ['keep_title', 'keep_hashTag', 'keep_data', 'keep_text']
    inlines = [SuggestionsInlines, FeedbackInlines]
    list_filter = ['keep_hashTag', 'keep_data']

class SearchLabelKeeperAdmin(admin.ModelAdmin):
    fields = ['searchlabelkeeper_marker']

class KeeperStatusAdmin(admin.ModelAdmin):
    fields = ['keeper_status_text']

admin.site.register(KeeperStatus, KeeperStatusAdmin)

admin.site.register(SearchLabelKeeper, SearchLabelKeeperAdmin)

admin.site.register(Keeper, KeeperAdmin)