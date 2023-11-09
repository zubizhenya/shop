from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError
from django.conf import settings


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name = 'title of the section')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Rubrics'
        verbose_name = 'Rubric'
        ordering = ['name']


class Bb(models.Model):
    class Kinds(models.TextChoices):
        BUY = 'b', 'Buy'
        SELL = 'sell', 'Sell'
        EXCHANGE = 'e', 'Exchange'
        __empty__ = 'Select the type of advertisement to be published'

    kind = models.CharField(max_length=10, choices=Kinds.choices, default=Kinds.SELL)
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Rubric', related_name='entries')
    title = models.CharField(max_length=50, verbose_name='Product')
    content = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.FloatField(null=True, blank=True, verbose_name='Price')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')
    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Please provide a description of the item being sold')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Specify non-negative prices')
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name_plural = 'Ads'
        verbose_name = 'Ad'
        ordering = ['-published']

class Notes(models.Model):
    bb = models.ForeignKey('Bb', null=True, on_delete=models.CASCADE, verbose_name='Product', related_name='product')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True, verbose_name='Comment')