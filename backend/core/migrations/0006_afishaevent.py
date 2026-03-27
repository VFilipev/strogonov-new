from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_guestfeedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='AfishaEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(
                    choices=[
                        ('main_event', 'Главное событие'),
                        ('masterclass', 'Мастер-класс'),
                    ],
                    max_length=32,
                    verbose_name='Тип',
                )),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('short_description', models.TextField(verbose_name='Краткое описание')),
                ('full_description', models.TextField(verbose_name='Полное описание')),
                ('event_date', models.DateField(verbose_name='Дата события')),
                ('price', models.DecimalField(
                    blank=True,
                    decimal_places=2,
                    help_text='Общая стоимость / билет (руб.)',
                    max_digits=12,
                    null=True,
                    verbose_name='Стоимость',
                )),
                ('price_per_guest', models.DecimalField(
                    blank=True,
                    decimal_places=2,
                    help_text='Стоимость на одного гостя (руб.)',
                    max_digits=12,
                    null=True,
                    verbose_name='Цена за гостя',
                )),
                ('image', models.ImageField(blank=True, null=True, upload_to='afisha/%Y/%m/', verbose_name='Изображение афиши')),
                ('order', models.PositiveIntegerField(
                    default=0,
                    help_text='При одинаковой дате — меньшее значение выше в списке',
                    verbose_name='Порядок',
                )),
                ('is_active', models.BooleanField(default=True, verbose_name='Показывать на сайте')),
            ],
            options={
                'verbose_name': 'Событие афиши',
                'verbose_name_plural': 'Афиша',
                'ordering': ['event_date', 'order', 'id'],
            },
        ),
    ]
