# Generated by Django 3.0.5 on 2020-04-21 15:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200421_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='policyruledestination',
            name='rule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dests', to='api.PolicyRule'),
        ),
    ]
