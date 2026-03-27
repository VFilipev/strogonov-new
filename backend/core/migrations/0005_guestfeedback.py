from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_galleryimage_active_unique_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(
                    choices=[
                        ('gratitude', 'Благодарность'),
                        ('complaint', 'Жалоба'),
                        ('question', 'Вопрос'),
                        ('suggestion', 'Предложение'),
                        ('other', 'Иное'),
                    ],
                    max_length=32,
                    verbose_name='Тема обращения',
                )),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='E-mail')),
                ('phone', models.CharField(blank=True, max_length=40, verbose_name='Телефон')),
                ('visit_date', models.DateField(blank=True, null=True, verbose_name='Дата посещения')),
                ('visit_time', models.CharField(blank=True, max_length=64, verbose_name='Время посещения')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='feedback/%Y/%m/', verbose_name='Вложение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
            ],
            options={
                'verbose_name': 'Обращение гостя',
                'verbose_name_plural': 'Обращения гостей',
                'ordering': ['-created_at'],
            },
        ),
    ]
