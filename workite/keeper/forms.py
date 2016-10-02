# -*- coding: utf-8 -*-
__author__ = 'macpro'

from django.forms import ModelForm
from django import forms
from keeper.models import Feedback, Keeper, SearchLabelKeeper

from ckeditor.widgets import CKEditorWidget




class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        #fields =  '__all__'
        fields = ['feedback_text']

class KeeperForm(ModelForm):
    class Meta:
        content = forms.CharField(widget=CKEditorWidget())
        model = Keeper
        fields = ['keep_text']

class SearchLabelKeeperForm(ModelForm):
    class Meta:
        model = SearchLabelKeeper
        fields = '__all__'

# from post.models import Post
#
# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=CKEditorWidget())
#     class Meta:
#         model = Post
#
# class PostAdmin(admin.ModelAdmin):
#     form = PostAdminForm
#
# admin.site.register(Post, PostAdmin)


