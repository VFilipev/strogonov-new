                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_afishaevent_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='site_active',
            field=models.BooleanField(default=True, help_text='Если выключено, на главной показывается режим технического обслуживания; бронирование остаётся доступным.', verbose_name='Сайт активен'),
        ),
    ]
