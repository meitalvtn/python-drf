# Generated by Django 3.0.5 on 2020-04-21 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200420_1454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rule',
            name='dests',
        ),
        migrations.CreateModel(
            name='RuleDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=60)),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Rule')),
            ],
        ),
    ]
