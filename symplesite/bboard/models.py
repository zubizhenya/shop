from django.db import models
from django.core import validators
from django.core.exceptions import ValidationError


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name = 'Название')
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']


class Bb(models.Model):
    class Kinds(models.TextChoices):
        BUY = 'b', 'Куплю'
        SELL = 'sell', 'Продам'
        EXCHANGE = 'e', 'Обменяю'
        __empty__ = 'Выберите тип публикуемого обьявления'

    kind = models.CharField(max_length=10, choices=Kinds.choices, default=Kinds.SELL)
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика', related_name='entries')
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите неотрицательные цены')
        if errors:
            raise ValidationError(errors)

    class Meta:
        verbose_name_plural = 'Обьявления'
        verbose_name = 'Обьявление'
        ordering = ['-published']

