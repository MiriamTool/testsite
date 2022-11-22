from django import forms

from django.forms.utils import ErrorList

from .models import News

from django.core.exceptions import ValidationError

import re

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="custom_errorlist">%s</div>' % ''.join(['<div class="custom_errorlist">%s</div>' % e for e in self])


class NewsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Выберите категорию'

    class Meta:
        model = News
        #fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

    def clean_is_published(self):
        is_published = self.cleaned_data['is_published']
        if not is_published:
            raise ValidationError('Новость должна быть отмечена, как опубликованная')
        return is_published
