# Generated by Django 4.2.11 on 2025-03-15 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='restaurant',
        ),
        migrations.RemoveField(
            model_name='table',
            name='restaurant',
        ),
        migrations.AlterField(
            model_name='table',
            name='capacity',
            field=models.IntegerField(default=4),
        ),
        migrations.AlterField(
            model_name='table',
            name='table_number',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='Restaurant',
        ),
    ]
