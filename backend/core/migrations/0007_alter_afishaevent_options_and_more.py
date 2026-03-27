                                             

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_afishaevent'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='afishaevent',
            options={'ordering': ['event_date', 'id'], 'verbose_name': 'Событие афиши', 'verbose_name_plural': 'Афиша'},
        ),
        migrations.RenameField(
            model_name='afishaevent',
            old_name='short_description',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='afishaevent',
            name='full_description',
        ),
        migrations.RemoveField(
            model_name='afishaevent',
            name='order',
        ),
        migrations.RemoveField(
            model_name='afishaevent',
            name='price',
        ),
    ]
