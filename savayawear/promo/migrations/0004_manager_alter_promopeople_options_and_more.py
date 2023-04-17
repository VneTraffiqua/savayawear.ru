# Generated by Django 4.2 on 2023-04-14 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo', '0003_alter_promopeople_telegram_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_id', models.IntegerField(verbose_name='Телеграм-ID менеджера')),
                ('fullname', models.CharField(help_text='Введите имя менеджера', max_length=100, verbose_name='Имя менеджера')),
            ],
            options={
                'verbose_name': 'менеджер',
                'verbose_name_plural': 'менеджеры',
            },
        ),
        migrations.AlterModelOptions(
            name='promopeople',
            options={'verbose_name': 'участника', 'verbose_name_plural': 'участники конкурса "200"'},
        ),
        migrations.AlterField(
            model_name='promopeople',
            name='fullname',
            field=models.CharField(help_text='Введите имя и фамилию участника', max_length=100, verbose_name='Имя и фамилия участника'),
        ),
        migrations.AlterField(
            model_name='promopeople',
            name='telegram_id',
            field=models.IntegerField(verbose_name='Телеграм-ID участника'),
        ),
    ]