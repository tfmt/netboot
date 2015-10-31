from netboot.base_views import FormView, TemplateView

from dist import forms
from dist.models import Category


class AddCategoryView(FormView):
    form_class = forms.AddCategoryForm
    require_login = True
    require_admin = True
    template_name = 'dist/add-category.html'

    def form_valid(self, form):
        try:
            Category.objects.get(
                title=form.cleaned_data['title'],
                parent=form.cleaned_data['parent'],
                owner=self.request.user
            )
        except Category.DoesNotExist:
            pass
        else:
            form.add_error('title', 'The title conflicts with an existing entry.')

        if form.is_valid():
            Category.objects.create(
                title=form.cleaned_data['title'],
                parent=form.cleaned_data['parent'],
                description=form.cleaned_data['description'],
                owner=self.request.user,
                is_active=form.cleaned_data['is_active']
            )

            return self.redirect('dist:index')
        else:
            return self.form_invalid(form)

    def get_form_kwargs(self):
        kwargs = super(AddCategoryView, self).get_form_kwargs()
        kwargs['parent_choices'] = self.get_parent_choices()
        return kwargs

    def get_initial(self):
        initial = super(AddCategoryView, self).get_initial()
        initial['is_active'] = 'yes'
        initial['is_public'] = 'no'
        return initial

    @staticmethod
    def get_parent_choices():
        choices = [('', 'No Parent')]

        def _add(category, level=0):
            choices.append((str(category.id), ('- ' * level) + category.title))

            for child in Category.objects.filter(parent=category):
                _add(child, level + 1)

        for category in Category.objects.filter(parent=None):
            _add(category)

        return choices


class IndexView(TemplateView):
    template_name = 'dist/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['root_categories'] = self.get_root_categories()
        return context

    @staticmethod
    def get_root_categories():
        return Category.objects.filter(parent=None)
