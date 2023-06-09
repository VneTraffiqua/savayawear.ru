# Generated by Django 4.2 on 2023-04-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PromoPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(verbose_name='Телеграм-ID докладчика')),
                ('fullname', models.CharField(help_text='Введите имя и фамилию докладчика', max_length=100, verbose_name='Имя и фамилия выступающего')),
                ('image', models.ImageField(upload_to='media/', verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'участника',
                'verbose_name_plural': 'участники',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.IntegerField(verbose_name='Телеграм-ID задающего вопрос')),
                ('question', models.TextField(verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'Вопросы',
            },
        ),
    ]
