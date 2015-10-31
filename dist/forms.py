from django import forms
from django.core.exceptions import ValidationError

from dist.models import Category

from netboot.forms import boolean_choices


class AddCategoryForm(forms.Form):
    parent = forms.ChoiceField(label='Parent', required=False)
    title = forms.CharField(max_length=100)
    description = forms.CharField(label='Description (optional)', required=False, widget=forms.Textarea)
    is_active = forms.ChoiceField(label='Is active?', choices=boolean_choices)
    is_public = forms.ChoiceField(label='Is public?', choices=boolean_choices)

    def __init__(self, parent_choices, **kwargs):
        super(AddCategoryForm, self).__init__(**kwargs)
        self.fields['parent'].choices = parent_choices

    def clean_parent(self):
        if self.cleaned_data.get('parent'):
            try:
                parent = Category.objects.get(id=int(self.cleaned_data['parent']))
            except Category.DoesNotExist:
                raise ValidationError('No such parent')
            else:
                return parent
        else:
            return None

    def clean_is_active(self):
        return self.cleaned_data['is_active'] == 'yes'

    def clean_is_public(self):
        return self.cleaned_data['is_public'] == 'yes'
