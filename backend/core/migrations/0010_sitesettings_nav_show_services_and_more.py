                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_sitesettings_site_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='nav_show_services',
            field=models.BooleanField(default=True, help_text='Ссылка на блок активного отдыха на главной.', verbose_name='Пункт «Услуги» в меню'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='nav_show_tours',
            field=models.BooleanField(default=True, help_text='Ссылка на страницу снегоходных туров.', verbose_name='Пункт «Туры» в меню'),
        ),
    ]
