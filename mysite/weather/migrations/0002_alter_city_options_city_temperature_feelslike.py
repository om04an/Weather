# Generated by Django 4.1.5 on 2023-01-19 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Town'},
        ),
        migrations.AddField(
            model_name='city',
            name='temperature_feelslike',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
