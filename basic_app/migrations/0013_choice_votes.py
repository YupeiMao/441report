# Generated by Django 2.1.7 on 2019-04-15 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0012_auto_20190414_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='votes',
            field=models.IntegerField(default=0),
        ),
    ]