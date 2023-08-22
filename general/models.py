from django.db import models


class Deal(models.Model):
    customer = models.CharField(max_length=256, verbose_name='Покупатель')
    stone_type = models.CharField(max_length=256, verbose_name='Вид камня')
    total_price = models.PositiveIntegerField(verbose_name='Сумма сделки')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    date = models.DateTimeField(verbose_name='Дата')

    def __str__(self):
        return f'{self.customer} {self.date}'
