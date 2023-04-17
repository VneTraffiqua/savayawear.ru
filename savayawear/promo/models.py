from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Manager(models.Model):
    telegram_id = models.IntegerField(
        verbose_name='Телеграм-ID менеджера'
    )
    fullname = models.CharField(
        max_length=100,
        help_text='Введите имя менеджера',
        verbose_name='Имя менеджера'
    )

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'менеджер'
        verbose_name_plural = 'менеджеры'


class PromoPeople(models.Model):
    telegram_id = models.IntegerField(
        verbose_name='Телеграм-ID участника',
    )
    fullname = models.CharField(
        max_length=100,
        help_text='Введите имя и фамилию участника',
        verbose_name='Имя и фамилия участника'
    )
    phone_numbers = PhoneNumberField(
        'Номер владельца', max_length=20, blank=True
    )

    image = models.ImageField(
        upload_to='media/', verbose_name='Изображение'
    )

    def __str__(self):
        return f'{self.fullname}'

    class Meta:
        verbose_name = 'участника'
        verbose_name_plural = 'участники конкурса "200"'


class Question(models.Model):
    telegram_user_id = models.IntegerField(
        verbose_name='Телеграм-ID задающего вопрос',
    )
    question = models.TextField(
        verbose_name='Вопрос'
    )

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'
