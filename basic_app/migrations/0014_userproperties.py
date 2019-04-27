# Generated by Django 2.1.7 on 2019-04-19 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0013_choice_votes'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_ratings', models.IntegerField()),
                ('work_balance_stars', models.IntegerField()),
                ('culture_values_stars', models.IntegerField()),
                ('career_opportunities_stars', models.IntegerField()),
                ('company_benefit_stars', models.IntegerField()),
                ('senior_management_stars', models.IntegerField()),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='basic_app.UserProfileInfo')),
            ],
        ),
    ]