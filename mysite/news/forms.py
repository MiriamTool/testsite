from django import forms

from django.forms.utils import ErrorList

from .models import Category

class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="custom_errorlist">%s</div>' % ''.join(['<div class="custom_errorlist">%s</div>' % e for e in self])


class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название новости', widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label='Текст новости', required=False, widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "rows": 5
        }))
    is_published = forms.BooleanField(label='Опубликовано?', initial=True)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Выберите категорию', widget=forms.Select(
        attrs={
            "class": "form-control"
        }))
