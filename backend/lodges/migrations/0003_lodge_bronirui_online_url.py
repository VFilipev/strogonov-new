                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodges', '0002_lodge_conveniences_lodge_include_lodgeavailability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodge',
            name='bronirui_online_url',
            field=models.URLField(blank=True, help_text='Если указана, кнопка «Забронировать» на сайте ведёт по этой ссылке', max_length=500, verbose_name='Ссылка на онлайн-бронирование'),
        ),
    ]
