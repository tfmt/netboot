from django.db import models
from django.utils import timezone


class Category(models.Model):
    class Meta:
        db_table = 'category'
        ordering = ('title',)

    title = models.CharField(max_length=100)
    parent = models.ForeignKey('self', null=True)
    description = models.TextField(null=True)
    owner = models.ForeignKey('user.User', null=True)
    is_public = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)

    @property
    def children(self):
        return Category.objects.filter(parent=self)
