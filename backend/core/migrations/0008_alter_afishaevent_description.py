                                             

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_afishaevent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afishaevent',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
    ]
